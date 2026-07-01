# Diabetes Risk Prediction

A supervised machine-learning project that predicts diabetes risk from 21 BRFSS 2015 health indicators using a **Random Forest classifier** and an interactive **Streamlit** web app.

> Educational project only — this is not a medical diagnostic tool.

---

## Results

| Metric | Value |
|---|---:|
| Test accuracy | 74.36% |
| Precision | 0.727 |
| Recall | 0.794 |
| F1 score | 0.759 |
| Clean records used | 69,057 |
| Input features | 21 |

Top learned risk factors: **General Health**, **High Blood Pressure**, **BMI**, **Age**, and **High Cholesterol**.

---

## Project structure

```text
diabetes-risk-prediction/
├── app/
│   └── streamlit_app.py
├── data/
│   └── diabetes_binary_5050split_health_indicators_BRFSS2015.csv
├── models/
│   ├── feature_names.json
│   ├── metrics.json
│   ├── model_comparison.csv
│   ├── model_comparison.json
│   └── rf_model.joblib
├── notebooks/
│   └── diabetes_analysis.ipynb
├── plots/
│   ├── 01_class_balance.png
│   ├── 02_bmi_distribution.png
│   ├── 03_bmi_boxplot.png
│   ├── 04_bp_chol.png
│   ├── 05_correlation_heatmap.png
│   ├── 06_confusion_matrix.png
│   ├── 07_feature_importance.png
│   └── 08_model_comparison.png
├── presentation/
│   ├── Diabetes_Final_Presentation.pdf
│   ├── Diabetes_Final_Presentation.pptx
│   └── Diabetes_Project_Report.pdf
├── scripts/
│   ├── compare_models.py
│   └── train_model.py
├── .streamlit/
│   └── config.toml
├── .gitignore
├── README.md
├── requirements.txt
└── runtime.txt
```

Only final project files are kept here. Duplicate reports, proposal drafts, reference screenshots, generated PowerPoint-building scripts, and the edited/missing-value duplicate CSV were removed from this GitHub-ready folder.

---

## Setup

```bash
git clone https://github.com/<your-username>/diabetes-risk-prediction.git
cd diabetes-risk-prediction
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Train the model

```bash
python scripts/train_model.py
```

The training script performs these steps:

1. Loads the CSV from `data/diabetes_binary_5050split_health_indicators_BRFSS2015.csv`.
2. Validates the expected 22 columns.
3. Cleans the dataset by dropping duplicates, removing missing/invalid rows, and fixing dtypes.
4. Saves EDA/evaluation plots in `plots/`.
5. Trains the Random Forest model.
6. Saves model artifacts in `models/`.

---

## Compare models

```bash
python scripts/compare_models.py
```

This compares Logistic Regression, Decision Tree, KNN, and Random Forest using the same cleaned data and same stratified train/test split.

---

## Run the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

Then open the local URL shown by Streamlit, usually: <http://localhost:8501>

---

## Dataset

CDC Behavioral Risk Factor Surveillance System (BRFSS) 2015 diabetes health indicators dataset, originally prepared by Alex Teboul on Kaggle.

---

## Main cleaning rule

The project uses the clean CSV from the Google Drive project folder. The code also includes defensive cleaning in `scripts/train_model.py` and the notebook:

- duplicate rows are removed;
- missing/edited cells are removed before dtype conversion;
- binary/ordinal survey fields are converted to integers;
- BMI is kept numeric;
- out-of-range survey codes are rejected.
