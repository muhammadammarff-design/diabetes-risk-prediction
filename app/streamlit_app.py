"""
Diabetes Risk Prediction - Streamlit Web App.

The app loads the trained Random Forest model and lets a user enter 21 health
indicators to receive a diabetes-risk prediction.

Run from the project root:
    streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# Configure the Streamlit page before any visible Streamlit output is created.
st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Resolve model paths from the app file location so the app works locally and on Streamlit Cloud.
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
MODEL_PATH = PROJECT_ROOT / "models" / "rf_model.joblib"
FEATURES_PATH = PROJECT_ROOT / "models" / "feature_names.json"
METRICS_PATH = PROJECT_ROOT / "models" / "metrics.json"


@st.cache_resource
def load_artifacts():
    """Load the trained model and metadata once, then reuse them on every rerun."""
    model = joblib.load(MODEL_PATH)
    feature_names = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return model, feature_names, metrics


try:
    model, feature_names, metrics = load_artifacts()
except FileNotFoundError:
    st.error("Trained model files were not found. Run `python scripts/train_model.py` first.")
    st.stop()

# Small CSS block for a cleaner medical-themed interface.
st.markdown(
    """
<style>
    .main { padding-top: 1rem; }
    .stButton button {
        background-color: #0F766E;
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border-radius: 6px;
    }
    .stButton button:hover { background-color: #0B4F4A; }
    h1 { color: #0F766E; }
    .metric-card {
        background: #F1F5F9;
        border-left: 4px solid #0F766E;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Page heading and short explanation for the user.
st.title("🩺 Diabetes Risk Prediction")
st.markdown(
    "Enter the patient's health information below. The model predicts diabetes risk "
    "from **21 BRFSS 2015 health indicators**."
)
st.markdown("---")

# Human-readable labels for coded BRFSS survey fields.
GENHLTH_OPTIONS = {1: "Excellent", 2: "Very good", 3: "Good", 4: "Fair", 5: "Poor"}
AGE_OPTIONS = {
    1: "18-24",
    2: "25-29",
    3: "30-34",
    4: "35-39",
    5: "40-44",
    6: "45-49",
    7: "50-54",
    8: "55-59",
    9: "60-64",
    10: "65-69",
    11: "70-74",
    12: "75-79",
    13: "80 or older",
}
EDUCATION_OPTIONS = {
    1: "Never attended school",
    2: "Elementary",
    3: "Some high school",
    4: "High-school graduate",
    5: "Some college",
    6: "College graduate",
}
INCOME_OPTIONS = {
    1: "< $10k",
    2: "$10k-15k",
    3: "$15k-20k",
    4: "$20k-25k",
    5: "$25k-35k",
    6: "$35k-50k",
    7: "$50k-75k",
    8: "> $75k",
}


# Convert Streamlit Yes/No answers into the 1/0 format used by the model.
def yes_no_to_int(answer: str) -> int:
    return 1 if answer == "Yes" else 0


with st.form("patient_form"):
    # Vital signs contain the strongest medical risk-factor inputs.
    st.subheader("Vital signs")
    col1, col2 = st.columns(2)
    high_bp = col1.radio("High blood pressure?", ["No", "Yes"], horizontal=True)
    high_chol = col2.radio("High cholesterol?", ["No", "Yes"], horizontal=True)
    chol_check = col1.radio("Cholesterol check in last 5 years?", ["No", "Yes"], index=1, horizontal=True)
    bmi = col2.slider("BMI (Body Mass Index)", 12, 60, 27)

    # Lifestyle fields capture smoking, exercise, diet, and alcohol behaviour.
    st.subheader("Lifestyle")
    col1, col2 = st.columns(2)
    smoker = col1.radio("Smoked at least 100 cigarettes in life?", ["No", "Yes"], horizontal=True)
    phys_activity = col2.radio("Physical activity in last 30 days?", ["No", "Yes"], index=1, horizontal=True)
    fruits = col1.radio("Eats fruit daily?", ["No", "Yes"], index=1, horizontal=True)
    veggies = col2.radio("Eats vegetables daily?", ["No", "Yes"], index=1, horizontal=True)
    heavy_alcohol = col1.radio("Heavy alcohol consumption?", ["No", "Yes"], horizontal=True)

    # Medical history fields capture existing conditions and access to care.
    st.subheader("Medical history")
    col1, col2 = st.columns(2)
    stroke = col1.radio("Ever had a stroke?", ["No", "Yes"], horizontal=True)
    heart_disease = col2.radio("Heart disease or heart attack?", ["No", "Yes"], horizontal=True)
    diff_walk = col1.radio("Difficulty walking or climbing stairs?", ["No", "Yes"], horizontal=True)
    any_healthcare = col2.radio("Has healthcare coverage?", ["No", "Yes"], index=1, horizontal=True)
    no_doc_cost = col1.radio("Skipped doctor due to cost in last year?", ["No", "Yes"], horizontal=True)

    # Self-reported health fields are coded exactly as in the BRFSS dataset.
    st.subheader("Self-reported health")
    col1, col2 = st.columns(2)
    gen_health = col1.selectbox(
        "General health",
        options=list(GENHLTH_OPTIONS.keys()),
        format_func=lambda value: f"{value} - {GENHLTH_OPTIONS[value]}",
        index=2,
    )
    mental_health = col2.slider("Poor mental-health days in last 30 days", 0, 30, 0)
    physical_health = col1.slider("Poor physical-health days in last 30 days", 0, 30, 0)

    # Demographic fields complete the 21-feature model input.
    st.subheader("Demographics")
    col1, col2, col3 = st.columns(3)
    sex = col1.radio("Sex", ["Female", "Male"], horizontal=True)
    age = col2.selectbox("Age group", options=list(AGE_OPTIONS.keys()), format_func=lambda value: AGE_OPTIONS[value], index=6)
    education = col3.selectbox(
        "Education",
        options=list(EDUCATION_OPTIONS.keys()),
        format_func=lambda value: EDUCATION_OPTIONS[value],
        index=4,
    )
    income = col1.selectbox(
        "Income bracket",
        options=list(INCOME_OPTIONS.keys()),
        format_func=lambda value: INCOME_OPTIONS[value],
        index=4,
    )

    submitted = st.form_submit_button("🔍 Predict Diabetes Risk")


if submitted:
    # Build one input row using the exact column names from training.
    raw_input = {
        "HighBP": yes_no_to_int(high_bp),
        "HighChol": yes_no_to_int(high_chol),
        "CholCheck": yes_no_to_int(chol_check),
        "BMI": bmi,
        "Smoker": yes_no_to_int(smoker),
        "Stroke": yes_no_to_int(stroke),
        "HeartDiseaseorAttack": yes_no_to_int(heart_disease),
        "PhysActivity": yes_no_to_int(phys_activity),
        "Fruits": yes_no_to_int(fruits),
        "Veggies": yes_no_to_int(veggies),
        "HvyAlcoholConsump": yes_no_to_int(heavy_alcohol),
        "AnyHealthcare": yes_no_to_int(any_healthcare),
        "NoDocbcCost": yes_no_to_int(no_doc_cost),
        "GenHlth": gen_health,
        "MentHlth": mental_health,
        "PhysHlth": physical_health,
        "DiffWalk": yes_no_to_int(diff_walk),
        "Sex": 1 if sex == "Male" else 0,
        "Age": age,
        "Education": education,
        "Income": income,
    }

    # Reorder columns using feature_names.json so prediction matches training order.
    input_frame = pd.DataFrame([raw_input])[feature_names]
    prediction = int(model.predict(input_frame)[0])
    diabetes_probability = float(model.predict_proba(input_frame)[0][1])

    st.markdown("---")
    st.subheader("Prediction result")

    if prediction == 1:
        st.error(f"⚠️ High risk of diabetes (probability ≈ {diabetes_probability:.1%})")
        st.markdown(
            "> The model predicts this patient is likely diabetic based on the provided indicators. "
            "A medical check-up such as HbA1c or fasting glucose is recommended."
        )
    else:
        st.success(f"✅ Low risk of diabetes (probability ≈ {diabetes_probability:.1%})")
        st.markdown(
            "> The model predicts this patient is unlikely diabetic based on the provided indicators. "
            "Maintaining a healthy lifestyle is still important for prevention."
        )

    # Show the class-1 probability visually for a quick interpretation.
    st.progress(diabetes_probability)
    st.caption(
        f"Probability breakdown: No Diabetes {1 - diabetes_probability:.1%} | "
        f"Diabetes {diabetes_probability:.1%}"
    )

# Sidebar displays the model details saved during training.
with st.sidebar:
    st.title("About this app")
    st.markdown(
        "This app uses a **Random Forest classifier** trained on the cleaned "
        "BRFSS 2015 diabetes-health-indicators dataset."
    )
    st.metric("Test accuracy", f"{metrics['test_accuracy'] * 100:.2f}%")
    st.metric("Records used", f"{metrics.get('records_used', 0):,}")
    st.metric("Features", metrics["n_features"])

    st.markdown("---")
    st.markdown("**Top 5 risk factors learned by the model**")
    for feature, score in metrics["top_5_features"].items():
        st.markdown(f"- **{feature}** · {score:.3f}")

    st.markdown("---")
    st.caption("Educational project only. Not a medical diagnostic tool.")
