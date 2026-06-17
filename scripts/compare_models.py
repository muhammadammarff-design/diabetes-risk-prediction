"""
Train and compare 4 supervised classifiers on the BRFSS diabetes dataset.
Saves a comparison table + bar-chart to plots/ and a JSON to models/.
"""

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

HERE         = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_PATH    = PROJECT_ROOT / "data" / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODELS_DIR   = PROJECT_ROOT / "models"
PLOTS_DIR    = PROJECT_ROOT / "plots"

# Style
TEAL = "#0F766E"
AMBER = "#F59E0B"
INK = "#1E293B"
SLATE = "#334155"
sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 200,
    "font.family": "DejaVu Sans",
    "axes.titleweight": "bold",
})

# ---------- data ----------
df = pd.read_csv(DATA_PATH).drop_duplicates().reset_index(drop=True)
int_cols = [c for c in df.columns if c != "BMI"]
df[int_cols] = df[int_cols].astype(int)
X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

models = {
    "Logistic\nRegression": (LogisticRegression(max_iter=1000, random_state=42), True),
    "Decision\nTree":       (DecisionTreeClassifier(max_depth=10, random_state=42), False),
    "K-Nearest\nNeighbors": (KNeighborsClassifier(n_neighbors=25, n_jobs=-1), True),
    "Random\nForest":       (RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=5, n_jobs=-1, random_state=42), False),
}

results = []
for name, (model, needs_scaling) in models.items():
    Xtr = X_train_s if needs_scaling else X_train
    Xte = X_test_s  if needs_scaling else X_test
    t0 = time.time()
    model.fit(Xtr, y_train)
    train_time = time.time() - t0
    y_pred = model.predict(Xte)
    results.append({
        "Model": name.replace("\n", " "),
        "Model_label": name,
        "Accuracy":  round(accuracy_score(y_test, y_pred), 4),
        "Precision": round(precision_score(y_test, y_pred), 4),
        "Recall":    round(recall_score(y_test, y_pred), 4),
        "F1":        round(f1_score(y_test, y_pred), 4),
        "TrainTime": round(train_time, 2),
    })
    print(f"{results[-1]['Model']:25s}  acc={results[-1]['Accuracy']:.4f}  f1={results[-1]['F1']:.4f}")

df_res = pd.DataFrame(results)
df_res.to_csv(MODELS_DIR / "model_comparison.csv", index=False)
with open(MODELS_DIR / "model_comparison.json", "w") as f:
    json.dump(results, f, indent=2)

# bar chart — Accuracy & F1
fig, ax = plt.subplots(figsize=(9.2, 4.8))
x = np.arange(len(df_res))
w = 0.36
b1 = ax.bar(x - w/2, df_res["Accuracy"], w, label="Accuracy", color=TEAL, edgecolor="white")
b2 = ax.bar(x + w/2, df_res["F1"], w, label="F1 score", color=AMBER, edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(df_res["Model_label"])
ax.set_ylim(0, 1.0)
ax.set_ylabel("Score")
ax.set_title("Model Comparison — Accuracy vs F1 Score", pad=14, color=INK)
ax.legend(frameon=True)
ax.grid(axis="y", alpha=0.35)

# value labels
for bars in [b1, b2]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.012, f"{h:.3f}",
                ha='center', va='bottom', fontsize=9, color=SLATE)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "08_model_comparison.png", dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("\n✅ Saved model_comparison.")
