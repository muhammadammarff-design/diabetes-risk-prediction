"""
Enhance plots — make them publication-quality and look like "real charts"
from a professional ML project report.

This script REGENERATES plots/01..08 with:
    - Cleaner styling (white background, teal accents)
    - Proper axis labels, legends, value labels
    - Larger fonts and bold titles
    - Better aspect ratios
    - Minimal gridlines (only where they help)
    - Direct use of the actual model outputs

Run:
    python scripts/enhance_plots.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_PATH = PROJECT_ROOT / "data" / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODELS_DIR = PROJECT_ROOT / "models"
PLOTS_DIR = PROJECT_ROOT / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# Professional palette
TEAL       = "#0F766E"
TEAL_DARK  = "#0B4F4A"
TEAL_LIGHT = "#14B8A6"
AMBER      = "#F59E0B"
AMBER_DK   = "#D97706"
SLATE      = "#475569"
INK        = "#1E293B"
MUTED      = "#94A3B8"
SOFT       = "#F1F5F9"
LINE       = "#E2E8F0"
GREEN_OK   = "#16A34A"
RED_NO     = "#DC2626"
BG         = "#FFFFFF"

sns.set_theme(style="white", font_scale=1.0)
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlepad": 14,
    "axes.labelsize": 11,
    "axes.labelweight": "regular",
    "axes.labelcolor": SLATE,
    "axes.edgecolor": LINE,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "savefig.bbox": "tight",
    "grid.color": LINE,
    "grid.linewidth": 0.6,
})

def save_fig(fig, name):
    out = PLOTS_DIR / name
    fig.tight_layout()
    fig.savefig(out, dpi=200, facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  saved {name}")

# =============================================================
# Load data
# =============================================================
print("Loading data...")
df = pd.read_csv(DATA_PATH).drop_duplicates().reset_index(drop=True)
int_cols = [c for c in df.columns if c != "BMI"]
df[int_cols] = df[int_cols].astype(int)
print(f"  shape = {df.shape}")

# =============================================================
# 01 — Class Balance
# =============================================================
fig, ax = plt.subplots(figsize=(6.4, 4.2))
counts = df["Diabetes_binary"].value_counts().sort_index()
total = counts.sum()
colors = [TEAL, AMBER]
bars = ax.bar(["No Diabetes", "Diabetes"], counts.values, color=colors,
              edgecolor="white", linewidth=1.2, width=0.55)
for bar, c in zip(bars, counts.values):
    pct = c / total * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + total*0.012,
            f"{c:,}", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=INK)
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f"{pct:.1f}%", ha="center", va="center",
            fontsize=11, fontweight="bold", color="white")
ax.set_title("Class Balance - Diabetes_binary (0/1)", pad=12, color=INK)
ax.set_ylabel("Count", color=SLATE)
ax.set_ylim(0, counts.max() * 1.15)
ax.grid(axis="y", alpha=0.35)
ax.set_axisbelow(True)
save_fig(fig, "01_class_balance.png")

# =============================================================
# 02 — BMI Distribution
# =============================================================
fig, ax = plt.subplots(figsize=(7.5, 4.6))
bins = np.arange(10, 55, 2)
for cls, label, color in [(0, "No Diabetes", TEAL), (1, "Diabetes", AMBER)]:
    sub = df[df["Diabetes_binary"] == cls]["BMI"]
    ax.hist(sub, bins=bins, alpha=0.55, color=color,
            edgecolor="white", linewidth=0.6, density=True)
    sub.plot.kde(ax=ax, color=color, linewidth=2.4, alpha=0.9, label=label)
ax.set_title("BMI Distribution by Diabetes Status", pad=12, color=INK)
ax.set_xlabel("Body Mass Index (BMI)", color=SLATE)
ax.set_ylabel("Density", color=SLATE)
ax.legend(frameon=True, framealpha=0.95, loc="upper right", fontsize=11, title="Diabetes Status")
ax.grid(axis="y", alpha=0.35)
ax.set_axisbelow(True)
ax.set_xlim(10, 55)
save_fig(fig, "02_bmi_distribution.png")

# =============================================================
# 03 — BMI Boxplot
# =============================================================
fig, ax = plt.subplots(figsize=(6.0, 4.4))
order = ["No Diabetes", "Diabetes"]
data = [df[df["Diabetes_binary"] == i]["BMI"] for i in (0, 1)]
bp = ax.boxplot(data, labels=order, patch_artist=True, widths=0.55,
                showmeans=True, meanprops={"marker":"D","markerfacecolor":"white",
                                           "markeredgecolor":INK,"markersize":7},
                medianprops={"color":"white","linewidth":2},
                whiskerprops={"color":SLATE,"linewidth":1.2},
                capprops={"color":SLATE,"linewidth":1.2},
                flierprops={"marker":"o","markerfacecolor":MUTED,
                            "markeredgecolor":"none","markersize":3,"alpha":0.5})
for patch, color in zip(bp["boxes"], [TEAL, AMBER]):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)
    patch.set_edgecolor("white")
medians = [np.median(d) for d in data]
for i, m in enumerate(medians, 1):
    ax.text(i + 0.18, m, f"median\n{m:.1f}", va="center", ha="left",
            fontsize=10, color=INK, fontweight="bold")
ax.set_title("BMI by Diabetes Status", pad=12, color=INK)
ax.set_ylabel("BMI", color=SLATE)
ax.set_xlabel("")
ax.grid(axis="y", alpha=0.35)
ax.set_axisbelow(True)
ax.set_ylim(10, 50)
save_fig(fig, "03_bmi_boxplot.png")

# =============================================================
# 04 — Risk factor counts (HighBP / HighChol)
# =============================================================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0))
for ax, col, title in zip(axes, ["HighBP", "HighChol"],
                           ["High Blood Pressure", "High Cholesterol"]):
    ct = pd.crosstab(df[col], df["Diabetes_binary"])
    ct = ct.reindex([0, 1])
    x = np.arange(len(ct.index))
    w = 0.38
    ax.bar(x - w/2, ct[0], w, label="No Diabetes", color=TEAL, edgecolor="white")
    ax.bar(x + w/2, ct[1], w, label="Diabetes", color=AMBER, edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(["No", "Yes"])
    ax.set_xlabel(f"{col} (0=No, 1=Yes)")
    ax.set_ylabel("Count")
    ax.set_title(title, pad=10, color=INK)
    ax.legend(frameon=True, framealpha=0.95, fontsize=10)
    ax.grid(axis="y", alpha=0.35); ax.set_axisbelow(True)
    for xi, vals in zip(x, [ct[0].values, ct[1].values]):
        for off, v in zip([-w/2, w/2], vals):
            ax.text(xi + off, v + max(vals)*0.015, f"{int(v):,}",
                    ha="center", va="bottom", fontsize=9, color=SLATE)
fig.suptitle("Risk Factors by Diabetes Status",
             fontsize=14, fontweight="bold", color=INK, y=1.02)
save_fig(fig, "04_bp_chol.png")

# =============================================================
# 05 — Correlation Heatmap
# =============================================================
fig, ax = plt.subplots(figsize=(11.5, 9.5))
corr = df.corr()
sns.heatmap(corr, ax=ax, cmap="RdBu_r", center=0, vmin=-0.5, vmax=0.5,
            square=True, linewidths=0.5, linecolor="white",
            cbar_kws={"shrink":0.72, "label":"Correlation"},
            annot=False, fmt=".2f")
ax.set_title("Correlation Matrix - BRFSS Health Indicators",
             pad=14, color=INK, fontsize=14)
plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor")
ax.tick_params(axis='x', labelsize=10, rotation=40)
ax.tick_params(axis='y', labelsize=10, rotation=0)
save_fig(fig, "05_correlation_heatmap.png")

# =============================================================
# Train models
# =============================================================
print("Training models...")
X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                    stratify=y, random_state=42)
scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_train)
X_te_s = scaler.transform(X_test)

# =============================================================
# 06 — Confusion Matrix (RF)
# =============================================================
rf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=5,
                            n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(5.4, 4.6))
disp = ConfusionMatrixDisplay(cm, display_labels=["No Diabetes", "Diabetes"])
disp.plot(ax=ax, cmap="GnBu", colorbar=False, values_format="d")
for txt in ax.texts:
    txt.set_fontsize(14)
    txt.set_fontweight("bold")
    txt.set_color(INK)
ax.set_title("Confusion Matrix - Random Forest", pad=12, color=INK, fontsize=14)
ax.set_xlabel("Predicted label", color=SLATE)
ax.set_ylabel("Actual label", color=SLATE)
save_fig(fig, "06_confusion_matrix.png")

# =============================================================
# 07 — Feature Importance
# =============================================================
imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8.5, 7.5))
top5_vals = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).head(5)
colors = [AMBER if f in list(top5_vals.index) else TEAL for f in imp.index]
bars = ax.barh(imp.index, imp.values, color=colors, edgecolor="white", linewidth=0.8)
ax.set_title("Random Forest - Feature Importance", pad=14, color=INK, fontsize=14)
ax.set_xlabel("Importance score", color=SLATE)
ax.grid(axis="x", alpha=0.35); ax.set_axisbelow(True)
ax.set_xlim(0, imp.max() * 1.20)
for bar in bars:
    w = bar.get_width()
    ax.text(w + imp.max()*0.01, bar.get_y() + bar.get_height()/2,
            f"{w:.3f}", va="center", ha="left", fontsize=9.5, color=SLATE)
ax.text(0.99, -0.18,
        "Top 5 highlighted in amber: " + ", ".join([f"{f} ({v:.3f})" for f, v in top5_vals.items()]),
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9.5, color=MUTED, style="italic")
save_fig(fig, "07_feature_importance.png")

# =============================================================
# 08 — Model Comparison
# =============================================================
models_dict = {
    "Logistic\nRegression":  (LogisticRegression(max_iter=1000, random_state=42), True),
    "Decision\nTree":        (DecisionTreeClassifier(max_depth=10, random_state=42), False),
    "K-Nearest\nNeighbors":  (KNeighborsClassifier(n_neighbors=25, n_jobs=-1), True),
    "Random\nForest":        (rf, False),
}
results = []
for name, (m, scale) in models_dict.items():
    Xtr = X_tr_s if scale else X_train
    Xte = X_te_s if scale else X_test
    m.fit(Xtr, y_train)
    pred = m.predict(Xte)
    results.append({
        "Model": name.replace("\n"," "),
        "Model_label": name,
        "Accuracy": round(accuracy_score(y_test, pred), 4),
        "Precision": round(precision_score(y_test, pred), 4),
        "Recall": round(recall_score(y_test, pred), 4),
        "F1": round(f1_score(y_test, pred), 4),
    })

df_res = pd.DataFrame(results)
with open(MODELS_DIR / "model_comparison.json", "w") as f:
    json.dump(results, f, indent=2)
df_res.to_csv(MODELS_DIR / "model_comparison.csv", index=False)

fig, ax = plt.subplots(figsize=(9.6, 5.0))
x = np.arange(len(df_res))
w = 0.36
b1 = ax.bar(x - w/2, df_res["Accuracy"], w, label="Accuracy", color=TEAL, edgecolor="white")
b2 = ax.bar(x + w/2, df_res["F1"], w, label="F1 score", color=AMBER, edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(df_res["Model_label"], fontsize=11)
ax.set_ylim(0, 1.0)
ax.set_ylabel("Score", color=SLATE)
ax.set_title("Model Comparison - Accuracy vs F1 Score", pad=14, color=INK, fontsize=14)
ax.legend(frameon=True, framealpha=0.95, loc="upper right", fontsize=11)
ax.grid(axis="y", alpha=0.35); ax.set_axisbelow(True)
for bars in [b1, b2]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.012, f"{h:.3f}",
                ha="center", va="bottom", fontsize=9.5, color=SLATE)
best_idx = int(df_res["F1"].idxmax())
ax.annotate("Best F1",
            xy=(best_idx + w/2, df_res["F1"].iloc[best_idx] + 0.04),
            xytext=(best_idx + w/2, df_res["F1"].iloc[best_idx] + 0.10),
            ha="center", fontsize=10, color=AMBER_DK, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=AMBER_DK, lw=1.2))
save_fig(fig, "08_model_comparison.png")

# Update metrics.json too
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1v = f1_score(y_test, y_pred)
metrics_obj = {
    "test_accuracy": round(float(acc), 4),
    "precision": round(float(prec), 4),
    "recall": round(float(rec), 4),
    "f1": round(float(f1v), 4),
    "test_size": int(len(y_test)),
    "n_features": int(X.shape[1]),
    "top_5_features": top5_vals.round(4).to_dict(),
}
with open(MODELS_DIR / "metrics.json", "w") as f:
    json.dump(metrics_obj, f, indent=2)

print("\nAll plots regenerated (enhanced, publication-quality).")
print(f"Top 5 features: {top5_vals.round(4).to_dict()}")
