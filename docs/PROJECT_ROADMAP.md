# Diabetes Risk Prediction — Complete Project Roadmap

**Group:** Ali Raza (2540010) · Muhammad Ammar (2540008) · Taha Ali (2540008)
**Instructor:** Sir Zaki · **Course:** Introduction to Data Science · **Semester:** 2

> This is your single source of truth. Follow this and the project is done.
> No work is split per person here — it's a shared roadmap. You can divide
> sub-tasks during the daily standup.

---

## TABLE OF CONTENTS
1. [Project Summary](#1-project-summary)
2. [Final Decisions (locked in)](#2-final-decisions-locked-in)
3. [Project Pipeline — the 6 phases](#3-project-pipeline--the-6-phases)
4. [Step-by-Step Implementation](#4-step-by-step-implementation)
5. [4-Week Timeline](#5-4-week-timeline)
6. [Deliverables Checklist](#6-deliverables-checklist)
7. [Risk Register & Mitigations](#7-risk-register--mitigations)
8. [Viva Q&A Preparation](#8-viva-qa-preparation)
9. [Definition of Done](#9-definition-of-done)

---

## 1. PROJECT SUMMARY

**One-sentence pitch:**
> We will train a Random Forest classifier on 70,693 BRFSS 2015 health
> survey records to predict whether a patient is at risk of diabetes,
> using only 21 lifestyle and clinical indicators.

**Why this matters (3 points for viva):**
1. Diabetes affects ~537 million adults worldwide; early prediction matters.
2. The model can power a low-cost screening tool that uses only survey
   answers — no lab tests required.
3. Identifying the top risk factors gives doctors actionable insights.

---

## 2. FINAL DECISIONS (locked in)

| Decision | Value | Why (justification for viva) |
|---|---|---|
| **Dataset** | `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` | Real CDC data, large (70k), pre-balanced, clean |
| **Learning type** | Supervised | Target column is labeled (0/1) |
| **Task type** | Binary Classification | Two classes: diabetic (1) vs not (0) |
| **Algorithm** | Random Forest Classifier | Handles mixed feature types, gives feature importance, beats Logistic Regression on this dataset (research validated) |
| **Accuracy target** | ≥ 80% on test set | Achievable on this data per published research |
| **Train/Test split** | 80 / 20, stratified | Standard, keeps class balance |
| **Evaluation metrics** | Accuracy · Confusion Matrix · Precision · Recall · F1 | More than just accuracy — important for medical context |
| **Tools** | Python · pandas · numpy · matplotlib · seaborn · scikit-learn · Jupyter | All from your course |
| **GUI** | Optional Phase 2 (Streamlit) | Only if Phase 1 is done early |

---

## 3. PROJECT PIPELINE — THE 6 PHASES

This matches the block diagram in your PPT. Each phase has clear inputs,
outputs, and a "Done when…" condition.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 01 DATA         │ →  │ 02 DATA         │ →  │ 03 EDA &        │
│    COLLECTION   │    │    CLEANING     │    │    CORRELATION  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 06 INSIGHTS &   │ ←  │ 05 MODEL        │ ←  │ 04 MODEL        │
│    REPORT       │    │    EVALUATION   │    │    TRAINING     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

| # | Phase | Done when… |
|---|---|---|
| 01 | Data Collection | CSV loaded into pandas, shape confirmed (70693, 22) |
| 02 | Data Cleaning | Duplicates removed, dtypes correct, missing values = 0 |
| 03 | EDA & Correlation | 6+ saved plots, correlation matrix, top-5 correlated features noted |
| 04 | Model Training | Random Forest trained on `X_train`, `y_train` |
| 05 | Model Evaluation | Accuracy, confusion matrix, classification report printed; test acc ≥ 0.80 |
| 06 | Insights & Report | Feature importance plot, written conclusions, final notebook clean |

---

## 4. STEP-BY-STEP IMPLEMENTATION

> Copy each block into a Jupyter Notebook cell in order. Comments explain
> each line. **Run the cells top to bottom — do not skip.**

### Step 0 — Setup
```python
# install once
# pip install pandas numpy matplotlib seaborn scikit-learn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, ConfusionMatrixDisplay)

sns.set_style("whitegrid")
pd.set_option("display.max_columns", None)
```

### Step 1 — Load the data (Phase 01)
```python
df = pd.read_csv("diabetes_binary_5050split_health_indicators_BRFSS2015.csv")
print("Shape:", df.shape)          # expect (70693, 22)
print("Columns:", list(df.columns))
df.head()
```
**Expected output:** shape `(70693, 22)` and 22 column names ending in
`Diabetes_binary` as the target.

### Step 2 — Describe & inspect (Phase 01)
```python
df.info()              # data types & non-null counts
df.describe()          # mean / std / min / max etc.
df['Diabetes_binary'].value_counts(normalize=True)   # ~50/50 confirmed
```

### Step 3 — Clean the data (Phase 02)
```python
# 3a) missing values  (this dataset has 0, but always check)
print("Missing per column:\n", df.isnull().sum())

# 3b) duplicate rows  (BRFSS has many — important to drop)
print("Duplicates before:", df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)
print("Duplicates after :", df.duplicated().sum())
print("New shape:", df.shape)

# 3c) data types — convert from float to int where it makes sense
int_cols = [c for c in df.columns if c != "BMI"]
df[int_cols] = df[int_cols].astype(int)
df.dtypes
```

### Step 4 — Exploratory Data Analysis (Phase 03)
```python
# 4a) class balance
plt.figure(figsize=(5,3))
sns.countplot(x="Diabetes_binary", data=df, palette=["#0F766E", "#F59E0B"])
plt.title("Class balance"); plt.tight_layout(); plt.savefig("01_class_balance.png")

# 4b) BMI distribution split by class
plt.figure(figsize=(7,4))
sns.histplot(data=df, x="BMI", hue="Diabetes_binary", bins=40, kde=True)
plt.title("BMI by Diabetes status"); plt.tight_layout(); plt.savefig("02_bmi_hist.png")

# 4c) boxplot of BMI vs class
plt.figure(figsize=(5,4))
sns.boxplot(x="Diabetes_binary", y="BMI", data=df)
plt.title("BMI distribution per class"); plt.tight_layout(); plt.savefig("03_bmi_box.png")

# 4d) bar chart of HighBP, HighChol counts split by class
fig, axes = plt.subplots(1, 2, figsize=(10,3))
sns.countplot(x="HighBP",   hue="Diabetes_binary", data=df, ax=axes[0])
sns.countplot(x="HighChol", hue="Diabetes_binary", data=df, ax=axes[1])
plt.tight_layout(); plt.savefig("04_bp_chol.png")
```

### Step 5 — Correlation analysis (Phase 03)
```python
corr = df.corr()

# 5a) full heatmap
plt.figure(figsize=(12,10))
sns.heatmap(corr, cmap="coolwarm", center=0, annot=False)
plt.title("Correlation matrix"); plt.tight_layout(); plt.savefig("05_heatmap.png")

# 5b) top correlations with the target — most important table for viva
top_corr = corr["Diabetes_binary"].drop("Diabetes_binary") \
                                   .abs().sort_values(ascending=False).head(10)
print("Top 10 features correlated with diabetes:\n", top_corr)
```

### Step 6 — Train / Test split (Phase 04) — **DO THIS BEFORE PREPROCESSING**
```python
X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,      # 20% test
    stratify=y,          # keep class balance in both splits
    random_state=42      # reproducibility
)
print("Train:", X_train.shape, "Test:", X_test.shape)
```

> 🔒 **Why split first?** Anything done to `X` before splitting (scaling,
> imputation, oversampling) leaks test info into training and inflates
> accuracy artificially. Random Forest doesn't need scaling, but the rule
> is universal — always split first.

### Step 7 — Train the Random Forest (Phase 04)
```python
model = RandomForestClassifier(
    n_estimators=200,        # 200 trees (good default)
    max_depth=15,            # limit depth → prevents overfitting
    min_samples_leaf=5,      # smoother trees
    n_jobs=-1,               # use all CPU cores
    random_state=42,
)
model.fit(X_train, y_train)
print("Training done.")
```

### Step 8 — Evaluate (Phase 05)
```python
y_pred = model.predict(X_test)

# 8a) accuracy
acc = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {acc:.4f}")     # expect ≈ 0.74 – 0.78 raw, higher with tuning

# 8b) confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)
ConfusionMatrixDisplay(cm, display_labels=["No Diabetes", "Diabetes"]).plot()
plt.title("Confusion matrix"); plt.tight_layout(); plt.savefig("06_confusion.png")

# 8c) precision / recall / F1
print(classification_report(y_test, y_pred,
                            target_names=["No Diabetes", "Diabetes"]))
```

### Step 9 — Feature Importance (Phase 06) — **the wow moment**
```python
importance = pd.Series(model.feature_importances_, index=X.columns) \
               .sort_values(ascending=True)
plt.figure(figsize=(7,8))
importance.plot(kind="barh", color="#0F766E")
plt.title("Random Forest feature importance"); plt.xlabel("Importance")
plt.tight_layout(); plt.savefig("07_importance.png")

print("Top 5 risk factors:")
print(importance.sort_values(ascending=False).head(5))
```

**Expected top 5 (from published research):** GenHlth, BMI, HighBP, Age, HighChol.

### Step 10 — Save the model (optional, for GUI phase)
```python
import joblib
joblib.dump(model, "rf_diabetes_model.pkl")
print("Model saved as rf_diabetes_model.pkl")
```

---

## 5. 4-WEEK TIMELINE

> Shared roadmap — divide subtasks each week during a 30-min standup.

| Week | Phase | Tasks | Output |
|---|---|---|---|
| **1** | 01 + 02 | Steps 1–3: load · inspect · clean · drop duplicates | `notebook_v1.ipynb` (clean df) |
| **2** | 03 | Steps 4–5: 6 saved plots + correlation table | 6 PNG files + correlation insights note |
| **3** | 04 + 05 | Steps 6–8: split · train RF · evaluate metrics | trained model + accuracy ≥ 0.80 |
| **4** | 06 | Step 9–10: feature importance + final report + final PPT (10–12 slides) | `final_notebook.ipynb` + `final_presentation.pptx` |

**Buffer:** Week 4 also holds the optional Streamlit GUI if time permits.

---

## 6. DELIVERABLES CHECKLIST

### For NEXT lab (proposal submission)
- [x] **`Diabetes_Project_Proposal.pptx`** (5 slides) ← already done
- [x] **`Diabetes_Project_Proposal.pdf`** (backup) ← already done
- [ ] All 3 group members rehearse 1–2 slides each

### For FINAL submission
- [ ] `final_notebook.ipynb` — runs end-to-end without errors
- [ ] `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` — dataset
- [ ] 7+ saved plots (PNG) — class balance, BMI hist, boxplot, bp/chol bars, heatmap, confusion, importance
- [ ] `rf_diabetes_model.pkl` — saved trained model
- [ ] `final_presentation.pptx` — 10–12 slides
- [ ] `README.md` — how to run the notebook

---

## 7. RISK REGISTER & MITIGATIONS

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Data leakage** (preprocessing before split) | Medium | Inflated accuracy → viva killer | Always split first (Step 6 enforces this) |
| **Not removing duplicates** | High on this dataset | Inflated test scores | `df.drop_duplicates()` in Step 3 |
| **Accuracy below 80%** | Low | Goal missed | We have `max_depth` + `n_estimators` to tune. Even 75% is publishable per research |
| **Overfitting** (train acc >> test acc) | Medium | Bad generalization | We use `max_depth=15`, `min_samples_leaf=5` |
| **Reporting only accuracy** | Medium | Teacher asks "what about false negatives?" | We always show confusion matrix + classification report |
| **Notebook breaks day of demo** | Low | Demo failure | Save all outputs as PNG; have PDF backup of final report |
| **Group member absent at viva** | Medium | Workload imbalance | Everyone learns ALL 9 steps, not just their share |

---

## 8. VIVA Q&A PREPARATION

| Likely question | Strong answer |
|---|---|
| What kind of problem is this? | Supervised learning, binary classification |
| Why this dataset? | Real CDC data, large (70k+), pre-balanced, clean, well-studied |
| Why Random Forest, not Logistic Regression? | Handles mixed feature types without scaling, gives feature importance for free, higher accuracy on this dataset (research validated) |
| What's a confusion matrix? | A 2×2 table of True/False Positives & Negatives |
| What does precision mean here? | Of all patients we *predicted* diabetic, what % really were |
| What does recall mean? | Of all *actual* diabetics, what % we correctly caught |
| Why is recall more important in medical apps? | Missing a real diabetic (false negative) is worse than a false alarm |
| Why did you drop duplicates? | Repeated rows inflate test accuracy artificially |
| Why split before preprocessing? | Prevents data leakage from test set into training |
| What's overfitting? | Model memorizes training data but fails on new data |
| How did you prevent overfitting? | `max_depth=15`, `min_samples_leaf=5`, and we report **test** accuracy not train |
| Top feature? | General Health (self-reported 1–5 scale), then BMI, HighBP, Age, HighChol |
| Would this replace a doctor? | No — it's a screening tool; final diagnosis needs lab tests (HbA1c, glucose) |
| Limitations of your model? | Self-reported survey data is noisy; no lab values; balanced data ≠ real-world prevalence (~14%) |

---

## 9. DEFINITION OF DONE

The project is **done** when **all** of these are true:

- [ ] Notebook runs top-to-bottom without errors on a fresh kernel
- [ ] Test accuracy ≥ 0.80 (or honestly reported lower with explanation)
- [ ] Confusion matrix, precision, recall, F1 all reported
- [ ] Top-5 risk factors plotted and discussed
- [ ] At least 6 visualizations saved as PNG
- [ ] Final 10–12 slide PowerPoint produced
- [ ] All 3 members can answer any question in §8

---

> **Files in this project folder:**
> - `Diabetes_Project_Proposal.pptx` — proposal deck (5 slides)
> - `Diabetes_Project_Proposal.pdf` — same, as PDF
> - `PROJECT_ROADMAP.md` — this document
> - `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` — dataset
