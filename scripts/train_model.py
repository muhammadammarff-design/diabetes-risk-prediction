"""
Train the Diabetes Risk Prediction model.

This script loads the BRFSS 2015 diabetes dataset, cleans the data, creates the
main EDA/evaluation plots, trains a Random Forest classifier, and saves the
artifacts used by the Streamlit app.

Run from the project root:
    python scripts/train_model.py
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

# Resolve paths from this file location so the script works from any terminal folder.
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_PATH = PROJECT_ROOT / "data" / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODELS_DIR = PROJECT_ROOT / "models"
PLOTS_DIR = PROJECT_ROOT / "plots"
MODELS_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

# The model must always see these columns in this exact order.
EXPECTED_COLUMNS = [
    "Diabetes_binary",
    "HighBP",
    "HighChol",
    "CholCheck",
    "BMI",
    "Smoker",
    "Stroke",
    "HeartDiseaseorAttack",
    "PhysActivity",
    "Fruits",
    "Veggies",
    "HvyAlcoholConsump",
    "AnyHealthcare",
    "NoDocbcCost",
    "GenHlth",
    "MentHlth",
    "PhysHlth",
    "DiffWalk",
    "Sex",
    "Age",
    "Education",
    "Income",
]

# Valid BRFSS coding ranges used to catch edited or accidentally added bad rows.
VALUE_RANGES = {
    "Diabetes_binary": (0, 1),
    "HighBP": (0, 1),
    "HighChol": (0, 1),
    "CholCheck": (0, 1),
    "BMI": (12, 98),
    "Smoker": (0, 1),
    "Stroke": (0, 1),
    "HeartDiseaseorAttack": (0, 1),
    "PhysActivity": (0, 1),
    "Fruits": (0, 1),
    "Veggies": (0, 1),
    "HvyAlcoholConsump": (0, 1),
    "AnyHealthcare": (0, 1),
    "NoDocbcCost": (0, 1),
    "GenHlth": (1, 5),
    "MentHlth": (0, 30),
    "PhysHlth": (0, 30),
    "DiffWalk": (0, 1),
    "Sex": (0, 1),
    "Age": (1, 13),
    "Education": (1, 6),
    "Income": (1, 8),
}

# Consistent plot colours used in every saved figure.
TEAL = "#0F766E"
AMBER = "#F59E0B"
SLATE = "#334155"
INK = "#1E293B"

# Make Matplotlib/Seaborn output readable for the report and presentation.
sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update(
    {
        "figure.dpi": 150,
        "savefig.dpi": 200,
        "font.family": "DejaVu Sans",
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "axes.labelcolor": SLATE,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def savefig(path: Path) -> None:
    """Save the current Matplotlib figure and close it to free memory."""
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  saved -> {path.relative_to(PROJECT_ROOT)}")


def load_and_clean_dataset(data_path: Path = DATA_PATH) -> tuple[pd.DataFrame, dict[str, object]]:
    """Load the CSV and perform all cleaning used by training and comparison.

    Cleaning is intentionally centralized here so the notebook, model training,
    and model-comparison script all follow the same logic:
    1. validate required columns,
    2. coerce edited values to numeric,
    3. drop duplicates,
    4. remove rows with missing values,
    5. remove rows outside valid BRFSS coding ranges,
    6. convert columns to correct dtypes.
    """
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    # Read the raw CSV exactly once so all later steps use the same dataframe.
    raw_df = pd.read_csv(data_path)
    records_loaded = int(len(raw_df))
    missing_cells_loaded = int(raw_df.isna().sum().sum())
    duplicate_rows_loaded = int(raw_df.duplicated().sum())

    # Stop early if the CSV structure is not the expected BRFSS dataset.
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in raw_df.columns]
    extra_columns = [col for col in raw_df.columns if col not in EXPECTED_COLUMNS]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Keep only the expected columns and preserve their order for modeling.
    df = raw_df[EXPECTED_COLUMNS].copy()

    # Convert text-like edited values to numeric; non-numeric values become NaN.
    df = df.apply(pd.to_numeric, errors="coerce")
    missing_rows_after_numeric = int(df.isna().any(axis=1).sum())

    # Remove exact duplicate records so a repeated patient row cannot bias training.
    rows_before_duplicates = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    duplicate_rows_removed = int(rows_before_duplicates - len(df))

    # Remove rows with missing values; this catches blank/edited cells before dtype conversion.
    rows_before_missing_drop = len(df)
    df = df.dropna().reset_index(drop=True)
    missing_rows_removed = int(rows_before_missing_drop - len(df))

    # Remove rows outside the allowed coding ranges or non-integer survey codes.
    valid_mask = pd.Series(True, index=df.index)
    invalid_counts: dict[str, int] = {}
    integer_columns = [col for col in EXPECTED_COLUMNS if col != "BMI"]
    for column, (low, high) in VALUE_RANGES.items():
        in_range = df[column].between(low, high)
        integer_like = np.isclose(df[column], np.round(df[column])) if column in integer_columns else True
        column_valid = in_range & integer_like
        invalid_counts[column] = int((~column_valid).sum())
        valid_mask &= column_valid

    invalid_rows_removed = int((~valid_mask).sum())
    df = df.loc[valid_mask].reset_index(drop=True)

    # Fix dtypes after missing/bad rows are removed.
    df[integer_columns] = df[integer_columns].round().astype(int)
    df["BMI"] = df["BMI"].astype(float)

    cleaning_summary = {
        "records_loaded": records_loaded,
        "records_used": int(len(df)),
        "missing_cells_loaded": missing_cells_loaded,
        "missing_rows_after_numeric": missing_rows_after_numeric,
        "duplicate_rows_loaded": duplicate_rows_loaded,
        "duplicate_rows_removed": duplicate_rows_removed,
        "missing_rows_removed": missing_rows_removed,
        "invalid_rows_removed": invalid_rows_removed,
        "invalid_values_by_column": invalid_counts,
        "extra_columns_ignored": extra_columns,
    }
    return df, cleaning_summary


def main() -> None:
    """Run the complete training pipeline."""
    print("\n" + "=" * 70)
    print("STEP 1 - Load and inspect the dataset")
    print("=" * 70)
    df_raw = pd.read_csv(DATA_PATH)
    print(f"Dataset path: {DATA_PATH}")
    print(f"Raw shape   : {df_raw.shape}")
    print(df_raw.head(3))
    print("\nRaw missing cells:", int(df_raw.isna().sum().sum()))
    print("Raw duplicate rows:", int(df_raw.duplicated().sum()))
    print("\nRaw dtypes:")
    print(df_raw.dtypes)

    print("\n" + "=" * 70)
    print("STEP 2 - Clean: drop duplicates, remove missing/bad rows, fix dtypes")
    print("=" * 70)
    df, cleaning_summary = load_and_clean_dataset(DATA_PATH)
    print(json.dumps(cleaning_summary, indent=2))
    print("\nClean shape:", df.shape)
    print("Clean dtypes:")
    print(df.dtypes)
    print("\nClean class balance:")
    print(df["Diabetes_binary"].value_counts(normalize=True).round(3))

    print("\n" + "=" * 70)
    print("STEP 3 - Exploratory Data Analysis plots")
    print("=" * 70)
    plt.figure(figsize=(5.5, 3.8))
    ax = sns.countplot(
        data=df,
        x="Diabetes_binary",
        hue="Diabetes_binary",
        palette={0: TEAL, 1: AMBER},
        legend=False,
        edgecolor="white",
        linewidth=0.8,
    )
    plt.title("Class Balance - Diabetes_binary", pad=12)
    plt.xlabel("Diabetes (0 = No, 1 = Yes)")
    plt.ylabel("Count")
    for bar in ax.patches:
        ax.annotate(
            f"{int(bar.get_height()):,}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=10,
            xytext=(0, 4),
            textcoords="offset points",
        )
    savefig(PLOTS_DIR / "01_class_balance.png")

    plt.figure(figsize=(7.5, 4.2))
    sns.histplot(
        data=df,
        x="BMI",
        hue="Diabetes_binary",
        bins=40,
        kde=True,
        palette={0: TEAL, 1: AMBER},
        alpha=0.65,
        edgecolor="white",
    )
    plt.title("BMI Distribution by Diabetes Status", pad=12)
    plt.xlabel("BMI")
    plt.ylabel("Frequency")
    savefig(PLOTS_DIR / "02_bmi_distribution.png")

    plt.figure(figsize=(5.5, 4.0))
    sns.boxplot(
        data=df,
        x="Diabetes_binary",
        y="BMI",
        hue="Diabetes_binary",
        palette={0: TEAL, 1: AMBER},
        legend=False,
        width=0.5,
    )
    plt.title("BMI by Diabetes Status", pad=12)
    plt.xlabel("Diabetes (0 = No, 1 = Yes)")
    plt.ylabel("BMI")
    savefig(PLOTS_DIR / "03_bmi_boxplot.png")

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    for axis, column, title in zip(
        axes,
        ["HighBP", "HighChol"],
        ["High Blood Pressure", "High Cholesterol"],
    ):
        sns.countplot(
            data=df,
            x=column,
            hue="Diabetes_binary",
            palette={0: TEAL, 1: AMBER},
            ax=axis,
            edgecolor="white",
        )
        axis.set_title(title, pad=10)
        axis.set_xlabel(f"{column} (0 = No, 1 = Yes)")
        axis.set_ylabel("Count")
        axis.legend(title="Diabetes", labels=["No", "Yes"])
    savefig(PLOTS_DIR / "04_bp_chol.png")

    print("\n" + "=" * 70)
    print("STEP 4 - Correlation analysis")
    print("=" * 70)
    corr = df.corr()
    plt.figure(figsize=(11, 8.5))
    sns.heatmap(
        corr,
        cmap="RdBu_r",
        center=0,
        vmin=-0.5,
        vmax=0.5,
        square=True,
        cbar_kws={"shrink": 0.72},
    )
    plt.title("Correlation Matrix - BRFSS Health Indicators", pad=14)
    savefig(PLOTS_DIR / "05_correlation_heatmap.png")

    top_corr = corr["Diabetes_binary"].drop("Diabetes_binary").abs().sort_values(ascending=False).head(10)
    print("\nTop 10 features correlated with Diabetes:")
    print(top_corr.round(3))

    print("\n" + "=" * 70)
    print("STEP 5 - Train/test split")
    print("=" * 70)
    X = df.drop("Diabetes_binary", axis=1)
    y = df["Diabetes_binary"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )
    print(f"Train: {X_train.shape} | Test: {X_test.shape}")

    print("\n" + "=" * 70)
    print("STEP 6 - Train Random Forest")
    print("=" * 70)
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_leaf=5,
        n_jobs=-1,
        random_state=42,
    )
    model.fit(X_train, y_train)
    print("Training complete.")

    print("\n" + "=" * 70)
    print("STEP 7 - Evaluate the model")
    print("=" * 70)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 score : {f1:.4f}")
    print("\nConfusion matrix:\n", cm)
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=["No Diabetes", "Diabetes"]))

    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ConfusionMatrixDisplay(cm, display_labels=["No Diabetes", "Diabetes"]).plot(
        ax=ax,
        cmap="GnBu",
        colorbar=False,
        values_format="d",
    )
    ax.set_title("Confusion Matrix - Random Forest", pad=12)
    savefig(PLOTS_DIR / "06_confusion_matrix.png")

    print("\n" + "=" * 70)
    print("STEP 8 - Feature importance")
    print("=" * 70)
    importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True)
    plt.figure(figsize=(7.5, 7.2))
    bars = plt.barh(importance.index, importance.values, color=TEAL)
    plt.title("Random Forest - Feature Importance", pad=14)
    plt.xlabel("Importance score")
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.003, bar.get_y() + bar.get_height() / 2, f"{width:.3f}", va="center", fontsize=9)
    plt.xlim(0, importance.max() * 1.18)
    savefig(PLOTS_DIR / "07_feature_importance.png")

    top5 = importance.sort_values(ascending=False).head(5)
    print("\nTop 5 features:")
    print(top5.round(4))

    print("\n" + "=" * 70)
    print("STEP 9 - Save model and metadata")
    print("=" * 70)
    joblib.dump(model, MODELS_DIR / "rf_model.joblib", compress=3)

    with open(MODELS_DIR / "feature_names.json", "w", encoding="utf-8") as file:
        json.dump(list(X.columns), file, indent=2)

    metrics = {
        "test_accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1": round(float(f1), 4),
        "records_used": int(len(df)),
        "test_size": int(len(y_test)),
        "n_features": int(X.shape[1]),
        "top_5_features": top5.round(4).to_dict(),
        "cleaning": cleaning_summary,
    }
    with open(MODELS_DIR / "metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print("Saved artifacts:")
    print("  models/rf_model.joblib")
    print("  models/feature_names.json")
    print("  models/metrics.json")
    print("Training pipeline finished successfully.")


if __name__ == "__main__":
    main()
