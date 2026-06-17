"""
================================================================
 Diabetes Risk Prediction  —  Training Script
================================================================
 Course   : Introduction to Data Science  (Semester 2)
 Group    : Ali Raza · Muhammad Ammar · Taha Ali
 Dataset  : diabetes_binary_5050split_health_indicators_BRFSS2015
 Model    : Random Forest Classifier (supervised, binary classification)

 What this script does (top to bottom):
   1.  Load the dataset
   2.  Inspect (shape, describe, missing, dtypes)
   3.  Clean (drop duplicates, fix dtypes)
   4.  Exploratory Data Analysis  →  saves PNG plots
   5.  Correlation analysis        →  saves heatmap + top features
   6.  Train / Test split           (80 / 20, stratified)
   7.  Train Random Forest
   8.  Evaluate (accuracy, confusion matrix, classification report)
   9.  Feature importance          →  saves plot + prints top 5
  10.  Save model (joblib) + feature names (json)

 How to run:
     cd diabetes_project
     python scripts/train_model.py

 Outputs go into:
     models/   →  rf_model.joblib   feature_names.json
     plots/    →  01_..png  02_..png  ...  07_..png
================================================================
"""

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score)
from sklearn.model_selection import train_test_split

# ----------------------------------------------------------------
# 0.  PROJECT PATHS
# ----------------------------------------------------------------
HERE         = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_PATH    = PROJECT_ROOT / "data" / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODELS_DIR   = PROJECT_ROOT / "models"
PLOTS_DIR    = PROJECT_ROOT / "plots"
MODELS_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------------------
# Plot style — professional, viva-ready
# ----------------------------------------------------------------
TEAL       = "#0F766E"
TEAL_LIGHT = "#14B8A6"
AMBER      = "#F59E0B"
SLATE      = "#334155"
INK        = "#1E293B"
BG         = "#FFFFFF"

sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "axes.labelcolor": SLATE,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
})

def savefig(path, **kw):
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  saved → {path.name}")

# ----------------------------------------------------------------
# STEP 1 :  LOAD THE DATA
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 1  —  Load the dataset")
print("="*60)
df = pd.read_csv(DATA_PATH)
print(f"Loaded {DATA_PATH.name}")
print(f"Shape : {df.shape}")
print(df.head(3))

# ----------------------------------------------------------------
# STEP 2 :  INSPECT
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 2  —  Inspect the data")
print("="*60)
df.info()
print("\n[ Describe ]\n", df.describe().round(2))
print("\n[ Missing values ]\n", df.isnull().sum().sum(), "total missing")
print("\n[ Class balance ]")
print(df["Diabetes_binary"].value_counts(normalize=True).round(3))

# ----------------------------------------------------------------
# STEP 3 :  CLEAN
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 3  —  Clean the data")
print("="*60)
dup_before = df.duplicated().sum()
print(f"Duplicates before: {dup_before}")
df = df.drop_duplicates().reset_index(drop=True)
print(f"Duplicates after : {df.duplicated().sum()}")
int_cols = [c for c in df.columns if c != "BMI"]
df[int_cols] = df[int_cols].astype(int)
print(f"Shape after cleaning: {df.shape}")

# ----------------------------------------------------------------
# STEP 4 :  EDA
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 4  —  Exploratory Data Analysis")
print("="*60)

# 4.1 Class balance
plt.figure(figsize=(5.5, 3.8))
ax = sns.countplot(x="Diabetes_binary", data=df, palette=[TEAL, AMBER], edgecolor="white", linewidth=0.8)
plt.title("Class Balance — Diabetes_binary", pad=12)
plt.xlabel("Diabetes (0 = No, 1 = Yes)")
plt.ylabel("Count")
for p in ax.patches:
    ax.annotate(f'{int(p.get_height()):,}', (p.get_x()+p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10, xytext=(0,4), textcoords='offset points')
savefig(PLOTS_DIR / "01_class_balance.png")

# 4.2 BMI distribution
plt.figure(figsize=(7.5, 4.2))
sns.histplot(data=df, x="BMI", hue="Diabetes_binary", bins=40, kde=True,
             palette=[TEAL, AMBER], alpha=0.65, edgecolor="white")
plt.title("BMI Distribution by Diabetes Status", pad=12)
plt.xlabel("BMI")
plt.ylabel("Frequency")
plt.legend(title="Diabetes", labels=["No", "Yes"])
savefig(PLOTS_DIR / "02_bmi_distribution.png")

# 4.3 BMI boxplot
plt.figure(figsize=(5.5, 4.0))
ax = sns.boxplot(x="Diabetes_binary", y="BMI", data=df, palette=[TEAL, AMBER], width=0.5)
plt.title("BMI by Diabetes Status", pad=12)
plt.xlabel("Diabetes (0 = No, 1 = Yes)")
plt.ylabel("BMI")
savefig(PLOTS_DIR / "03_bmi_boxplot.png")

# 4.4 Risk factors
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
for ax, col, title in zip(axes, ["HighBP", "HighChol"], ["High Blood Pressure", "High Cholesterol"]):
    sns.countplot(x=col, hue="Diabetes_binary", data=df, palette=[TEAL, AMBER], ax=ax, edgecolor="white")
    ax.set_title(title, pad=10)
    ax.set_xlabel(f"{col} (0=No, 1=Yes)")
    ax.legend(title="Diabetes", labels=["No","Yes"])
plt.tight_layout()
plt.savefig(PLOTS_DIR / "04_bp_chol.png", dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f"  saved → 04_bp_chol.png")

print(f"Saved EDA plots → {PLOTS_DIR}")

# ----------------------------------------------------------------
# STEP 5 :  CORRELATION
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 5  —  Correlation analysis")
print("="*60)
corr = df.corr()
plt.figure(figsize=(11, 8.5))
sns.heatmap(corr, cmap="RdBu_r", center=0, vmin=-0.5, vmax=0.5,
            square=True, cbar_kws={"shrink": 0.72})
plt.title("Correlation Matrix — BRFSS Health Indicators", pad=14)
savefig(PLOTS_DIR / "05_correlation_heatmap.png")

top_corr = (corr["Diabetes_binary"].drop("Diabetes_binary")
            .abs().sort_values(ascending=False).head(10))
print("\n[ Top 10 features correlated with Diabetes ]")
print(top_corr.round(3))

# ----------------------------------------------------------------
# STEP 6 :  TRAIN / TEST SPLIT
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 6  —  Train / Test split")
print("="*60)
X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42)
print(f"Train: {X_train.shape}   Test: {X_test.shape}")

# ----------------------------------------------------------------
# STEP 7 :  TRAIN
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 7  —  Train Random Forest")
print("="*60)
model = RandomForestClassifier(
    n_estimators=200, max_depth=15, min_samples_leaf=5,
    n_jobs=-1, random_state=42)
model.fit(X_train, y_train)
print("Training done.")

# ----------------------------------------------------------------
# STEP 8 :  EVALUATE
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 8  —  Evaluate")
print("="*60)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print(f"\nAccuracy : {acc:.4f}  Precision: {prec:.4f}  Recall: {rec:.4f}  F1: {f1:.4f}")
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion matrix:\n", cm)
print("\n", classification_report(y_test, y_pred, target_names=["No Diabetes","Diabetes"]))

# Confusion matrix plot - clean
fig, ax = plt.subplots(figsize=(4.8, 4.2))
ConfusionMatrixDisplay(cm, display_labels=["No Diabetes", "Diabetes"]).plot(
    ax=ax, cmap="GnBu", colorbar=False, values_format="d")
ax.set_title("Confusion Matrix — Random Forest", pad=12)
savefig(PLOTS_DIR / "06_confusion_matrix.png")

# ----------------------------------------------------------------
# STEP 9 :  FEATURE IMPORTANCE
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 9  —  Feature importance")
print("="*60)
importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True)
plt.figure(figsize=(7.5, 7.2))
bars = plt.barh(importance.index, importance.values, color=TEAL)
plt.title("Random Forest — Feature Importance", pad=14)
plt.xlabel("Importance score")
# add value labels
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.003, bar.get_y() + bar.get_height()/2, f"{w:.3f}",
             va='center', fontsize=9, color=SLATE)
plt.xlim(0, importance.max()*1.18)
savefig(PLOTS_DIR / "07_feature_importance.png")

top5 = importance.sort_values(ascending=False).head(5)
print("\nTop 5:\n", top5.round(4))

# ----------------------------------------------------------------
# STEP 10 :  SAVE MODEL
# ----------------------------------------------------------------
print("\n" + "="*60)
print(" STEP 10  —  Save model & metadata")
print("="*60)
# compress=3 keeps the file ~18 MB (well under GitHub's 25 MB web-upload limit)
joblib.dump(model, MODELS_DIR / "rf_model.joblib", compress=3)
with open(MODELS_DIR / "feature_names.json", "w") as f:
    json.dump(list(X.columns), f, indent=2)
with open(MODELS_DIR / "metrics.json", "w") as f:
    json.dump({
        "test_accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1": round(float(f1), 4),
        "test_size": int(len(y_test)),
        "n_features": int(X.shape[1]),
        "top_5_features": top5.round(4).to_dict(),
    }, f, indent=2)
print("✅  Training complete.")
