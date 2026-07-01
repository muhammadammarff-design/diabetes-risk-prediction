"""
Compare four supervised machine-learning models on the cleaned diabetes dataset.

Run from the project root:
    python scripts/compare_models.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# Reuse the same data path, cleaning function, plot folder, and colours as training.
from train_model import AMBER, DATA_PATH, MODELS_DIR, PLOTS_DIR, SLATE, TEAL, load_and_clean_dataset


def main() -> None:
    """Train several models and save their comparison metrics/plot."""
    MODELS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)

    # Clean the dataset exactly the same way as scripts/train_model.py.
    df, cleaning_summary = load_and_clean_dataset(DATA_PATH)
    print("Cleaning summary:")
    print(json.dumps(cleaning_summary, indent=2))

    # Split the target column from the 21 input features.
    X = df.drop("Diabetes_binary", axis=1)
    y = df["Diabetes_binary"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    # Logistic Regression and KNN need scaled features; tree models do not.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Each tuple stores the model object and whether it needs scaled input.
    candidate_models = {
        "Logistic\nRegression": (LogisticRegression(max_iter=1000, random_state=42), True),
        "Decision\nTree": (DecisionTreeClassifier(max_depth=10, random_state=42), False),
        "K-Nearest\nNeighbors": (KNeighborsClassifier(n_neighbors=25, n_jobs=-1), True),
        "Random\nForest": (
            RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_leaf=5,
                n_jobs=-1,
                random_state=42,
            ),
            False,
        ),
    }

    results: list[dict[str, float | str]] = []
    for name, (model, needs_scaling) in candidate_models.items():
        # Choose scaled or unscaled data depending on model requirements.
        train_features = X_train_scaled if needs_scaling else X_train
        test_features = X_test_scaled if needs_scaling else X_test

        # Time training so the comparison includes speed as well as accuracy.
        start_time = time.time()
        model.fit(train_features, y_train)
        train_time = time.time() - start_time

        # Evaluate on the same untouched test split for a fair comparison.
        y_pred = model.predict(test_features)
        result = {
            "Model": name.replace("\n", " "),
            "Model_label": name,
            "Accuracy": round(accuracy_score(y_test, y_pred), 4),
            "Precision": round(precision_score(y_test, y_pred), 4),
            "Recall": round(recall_score(y_test, y_pred), 4),
            "F1": round(f1_score(y_test, y_pred), 4),
            "TrainTime": round(train_time, 2),
        }
        results.append(result)
        print(f"{result['Model']:25s} acc={result['Accuracy']:.4f} f1={result['F1']:.4f}")

    # Save the numerical results for the report, README, and future checking.
    comparison_df = pd.DataFrame(results)
    comparison_df.to_csv(MODELS_DIR / "model_comparison.csv", index=False)
    with open(MODELS_DIR / "model_comparison.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    # Create a grouped bar chart comparing Accuracy and F1 score.
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    x = np.arange(len(comparison_df))
    width = 0.36
    accuracy_bars = ax.bar(
        x - width / 2,
        comparison_df["Accuracy"],
        width,
        label="Accuracy",
        color=TEAL,
        edgecolor="white",
    )
    f1_bars = ax.bar(
        x + width / 2,
        comparison_df["F1"],
        width,
        label="F1 score",
        color=AMBER,
        edgecolor="white",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(comparison_df["Model_label"])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Score")
    ax.set_title("Model Comparison - Accuracy vs F1 Score", pad=14)
    ax.legend(frameon=True)
    ax.grid(axis="y", alpha=0.35)

    # Write each bar value above the bar for easier reading in the presentation.
    for bars in [accuracy_bars, f1_bars]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.012,
                f"{height:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
                color=SLATE,
            )

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "08_model_comparison.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()

    print("\nSaved comparison outputs:")
    print("  models/model_comparison.csv")
    print("  models/model_comparison.json")
    print("  plots/08_model_comparison.png")


if __name__ == "__main__":
    main()
