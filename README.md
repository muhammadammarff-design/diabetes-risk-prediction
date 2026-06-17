# 🩺 Diabetes Risk Prediction

A supervised machine-learning project that predicts diabetes risk from 21 patient health indicators (BRFSS 2015) using a **Random Forest** classifier — with an interactive **Streamlit** web app.

> **Course:** Introduction to Data Science · **Semester:** 2  
> **Group:** Ali Raza (2540010) · Muhammad Ammar (2540008) · Taha Ali (2540008)  
> **Instructor:** Sir Zaki

---

## 📊 Results

| Metric | Value |
|---|---|
| Test accuracy | **74.36 %** |
| Precision | 0.727 |
| Recall | 0.794 |
| F1 Score | **0.759** |
| Records used  | 69,057 (after duplicate removal) |
| Features      | 21 health indicators |
| Top 5 risk factors | General Health · High BP · BMI · Age · High Cholesterol |

4 models compared: Logistic Regression (74.5% acc), Decision Tree (73.2%), KNN (73.5%), **Random Forest (74.4%, best F1)**

---

## 📁 Project Structure

```
Diabetes_Project/
├── app/
│   └── streamlit_app.py          # interactive Streamlit web app
├── data/
│   └── diabetes_binary_5050split_health_indicators_BRFSS2015.csv
├── models/
│   ├── rf_model.joblib           # trained Random Forest
│   ├── feature_names.json
│   ├── metrics.json
│   ├── model_comparison.csv
│   └── model_comparison.json
├── notebooks/
│   └── diabetes_analysis.ipynb
├── plots/                        # 8 publication-quality PNGs
│   ├── 01_class_balance.png
│   ├── 02_bmi_distribution.png
│   ├── 03_bmi_boxplot.png
│   ├── 04_bp_chol.png
│   ├── 05_correlation_heatmap.png
│   ├── 06_confusion_matrix.png
│   ├── 07_feature_importance.png
│   └── 08_model_comparison.png
├── presentation/
│   ├── Diabetes_Final_Presentation.pptx  # 17 slides, speaker notes
│   ├── Diabetes_Final_Presentation.pdf
│   ├── Diabetes_Project_Proposal.pptx
│   └── Diabetes_Project_Proposal.pdf
├── scripts/
│   ├── train_model.py            # train RF + generate plots 01-07
│   ├── compare_models.py         # compare 4 models, plot 08
│   └── build_ppt_clean.py        # rebuild final PPT (no repair mode)
├── docs/
│   ├── Speaker_Notes.md          # full viva speaker notes
│   ├── SETUP_GUIDE.md            # local + GitHub + Streamlit Cloud
│   └── PROJECT_ROADMAP.md
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & set up

```bash
git clone https://github.com/<your-username>/diabetes-risk-prediction.git
cd diabetes-risk-prediction
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Train the model

```bash
python scripts/train_model.py
```
Creates `models/rf_model.joblib`, metrics, and 7 PNG plots in `plots/`.

### 3. Compare 4 models (optional)

```bash
python scripts/compare_models.py
```
Creates `plots/08_model_comparison.png` and `models/model_comparison.json`

### 4. Launch the web app

```bash
streamlit run app/streamlit_app.py
```
Open http://localhost:8501

### 5. Rebuild the presentation

```bash
pip install python-pptx
python scripts/build_ppt_clean.py
```
Output: `presentation/Diabetes_Final_Presentation.pptx` — 17 slides, speaker notes, 100% PowerPoint compatible (no repair prompt).

---

## 🧠 Methodology

| Phase | Step | Output |
|---|---|---|
| 01 | Data Collection | Load CSV (70,693 × 22) |
| 02 | Data Cleaning   | Drop 1,636 duplicates → 69,057 rows |
| 03 | EDA & Correlation | 5 EDA plots + heatmap |
| 04 | Model Training  | Random Forest (200 trees, depth 15) |
| 05 | Model Evaluation| Accuracy, Precision, Recall, F1, Confusion Matrix |
| 06 | Feature Importance | Top-5 risk factors |
| 07 | Deployment | Streamlit web app |

**Why Random Forest?** Handles mixed types without scaling, built-in feature importance, robust to noisy survey data, best F1 score (0.759).

---

## 📚 Dataset

CDC Behavioral Risk Factor Surveillance System (BRFSS) 2015 — cleaned by Alex Teboul:  
https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset

---

## 📖 Documentation

- **Setup:** `docs/SETUP_GUIDE.md` — local install, GitHub push, Streamlit Cloud deploy
- **Roadmap:** `docs/PROJECT_ROADMAP.md`
- **Speaker Notes:** `docs/Speaker_Notes.md` — slide-by-slide viva script
- Speaker notes are also embedded in the PPT (View → Notes Page)

---

## ⚠️ Disclaimer

Educational project only. Not a medical diagnostic tool. Consult a qualified healthcare professional.

