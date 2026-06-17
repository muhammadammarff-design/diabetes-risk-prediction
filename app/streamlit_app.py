"""
================================================================
 Diabetes Risk Prediction  —  Streamlit Web App
================================================================
 Loads the trained Random Forest model and lets the user enter
 their health information through a clean form to get a
 real-time diabetes-risk prediction.

 How to run:
     cd diabetes_project
     streamlit run app/streamlit_app.py
================================================================
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------
# PAGE CONFIG (must be the first Streamlit call)
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------
# LOAD MODEL + METADATA  (cached so it loads only once)
# ----------------------------------------------------------------
HERE         = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
MODEL_PATH   = PROJECT_ROOT / "models" / "rf_model.joblib"
FEATURES_PATH= PROJECT_ROOT / "models" / "feature_names.json"
METRICS_PATH = PROJECT_ROOT / "models" / "metrics.json"

@st.cache_resource
def load_artifacts():
    model         = joblib.load(MODEL_PATH)
    feature_names = json.loads(FEATURES_PATH.read_text())
    metrics       = json.loads(METRICS_PATH.read_text())
    return model, feature_names, metrics

try:
    model, feature_names, metrics = load_artifacts()
except FileNotFoundError:
    st.error("❌ Trained model not found. Please run `python scripts/train_model.py` first.")
    st.stop()


# ----------------------------------------------------------------
# CUSTOM CSS — clean medical look
# ----------------------------------------------------------------
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .stButton button {
        background-color: #0F766E; color: white; border: none;
        padding: 0.6rem 1.5rem; font-weight: 600; border-radius: 6px;
    }
    .stButton button:hover { background-color: #0B4F4A; }
    h1 { color: #0F766E; }
    .metric-card {
        background: #F1F5F9; border-left: 4px solid #0F766E;
        padding: 1rem; border-radius: 4px; margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------
st.title("🩺 Diabetes Risk Prediction")
st.markdown(
    "*Enter the patient's health information below. The model will predict "
    "the likelihood of diabetes based on **21 health indicators** from the "
    "BRFSS 2015 dataset.*"
)
st.markdown("---")


# ----------------------------------------------------------------
# INPUT FORM  —  organised in 3 expandable sections
# ----------------------------------------------------------------
# Human-readable options for ordinal columns
GENHLTH_OPTS = {1: "Excellent", 2: "Very good", 3: "Good", 4: "Fair", 5: "Poor"}
AGE_OPTS = {
    1:"18-24", 2:"25-29", 3:"30-34", 4:"35-39", 5:"40-44", 6:"45-49",
    7:"50-54", 8:"55-59", 9:"60-64", 10:"65-69", 11:"70-74",
    12:"75-79", 13:"80 or older",
}
EDU_OPTS = {
    1:"Never attended school", 2:"Elementary", 3:"Some high school",
    4:"High-school grad", 5:"Some college", 6:"College graduate",
}
INCOME_OPTS = {
    1:"< $10k",  2:"$10k-15k", 3:"$15k-20k", 4:"$20k-25k",
    5:"$25k-35k", 6:"$35k-50k", 7:"$50k-75k", 8:"> $75k",
}

with st.form("patient_form"):

    st.subheader("Vital signs")
    c1, c2 = st.columns(2)
    HighBP   = c1.radio("High blood pressure?",          ["No", "Yes"], horizontal=True)
    HighChol = c2.radio("High cholesterol?",             ["No", "Yes"], horizontal=True)
    CholCheck= c1.radio("Cholesterol check in 5 years?", ["No", "Yes"], index=1, horizontal=True)
    BMI      = c2.slider("BMI (Body Mass Index)", 12, 60, 27)

    st.subheader("Lifestyle")
    c1, c2 = st.columns(2)
    Smoker        = c1.radio("Smoked ≥100 cigarettes in life?", ["No","Yes"], horizontal=True)
    PhysActivity  = c2.radio("Physical activity in last 30 days?",["No","Yes"], index=1, horizontal=True)
    Fruits        = c1.radio("Eats fruit daily?",               ["No","Yes"], index=1, horizontal=True)
    Veggies       = c2.radio("Eats vegetables daily?",          ["No","Yes"], index=1, horizontal=True)
    HvyAlcohol    = c1.radio("Heavy alcohol consumption?",      ["No","Yes"], horizontal=True)

    st.subheader("Medical history")
    c1, c2 = st.columns(2)
    Stroke              = c1.radio("Ever had a stroke?",       ["No","Yes"], horizontal=True)
    HeartDiseaseorAttack= c2.radio("Heart disease or attack?", ["No","Yes"], horizontal=True)
    DiffWalk            = c1.radio("Difficulty walking/climbing stairs?", ["No","Yes"], horizontal=True)
    AnyHealthcare       = c2.radio("Has healthcare coverage?", ["No","Yes"], index=1, horizontal=True)
    NoDocbcCost         = c1.radio("Skipped doctor due to cost (last year)?", ["No","Yes"], horizontal=True)

    st.subheader("Self-reported health")
    c1, c2 = st.columns(2)
    GenHlth   = c1.selectbox("General health", options=list(GENHLTH_OPTS.keys()),
                             format_func=lambda x: f"{x} — {GENHLTH_OPTS[x]}", index=2)
    MentHlth  = c2.slider("Poor mental-health days (last 30 days)", 0, 30, 0)
    PhysHlth  = c1.slider("Poor physical-health days (last 30 days)", 0, 30, 0)

    st.subheader("Demographics")
    c1, c2, c3 = st.columns(3)
    Sex       = c1.radio("Sex", ["Female", "Male"], horizontal=True)
    Age       = c2.selectbox("Age group", options=list(AGE_OPTS.keys()),
                             format_func=lambda x: AGE_OPTS[x], index=6)
    Education = c3.selectbox("Education", options=list(EDU_OPTS.keys()),
                             format_func=lambda x: EDU_OPTS[x], index=4)
    Income    = c1.selectbox("Income bracket", options=list(INCOME_OPTS.keys()),
                             format_func=lambda x: INCOME_OPTS[x], index=4)

    st.markdown(" ")
    submitted = st.form_submit_button("🔍 Predict Diabetes Risk")


# ----------------------------------------------------------------
# PREDICTION
# ----------------------------------------------------------------
def yn(x):  # "Yes"/"No" → 1/0
    return 1 if x == "Yes" else 0

if submitted:
    # Build the input row in the EXACT column order the model expects
    raw = {
        "HighBP":               yn(HighBP),
        "HighChol":             yn(HighChol),
        "CholCheck":            yn(CholCheck),
        "BMI":                  BMI,
        "Smoker":               yn(Smoker),
        "Stroke":               yn(Stroke),
        "HeartDiseaseorAttack": yn(HeartDiseaseorAttack),
        "PhysActivity":         yn(PhysActivity),
        "Fruits":               yn(Fruits),
        "Veggies":              yn(Veggies),
        "HvyAlcoholConsump":    yn(HvyAlcohol),
        "AnyHealthcare":        yn(AnyHealthcare),
        "NoDocbcCost":          yn(NoDocbcCost),
        "GenHlth":              GenHlth,
        "MentHlth":             MentHlth,
        "PhysHlth":             PhysHlth,
        "DiffWalk":             yn(DiffWalk),
        "Sex":                  1 if Sex == "Male" else 0,
        "Age":                  Age,
        "Education":            Education,
        "Income":               Income,
    }
    # Reorder according to feature_names → critical to avoid bugs
    X_input = pd.DataFrame([raw])[feature_names]

    pred  = int(model.predict(X_input)[0])
    proba = float(model.predict_proba(X_input)[0][1])     # probability of class 1

    st.markdown("---")
    st.subheader("Prediction result")

    if pred == 1:
        st.error(f"⚠️  **High risk of diabetes**   "
                 f"(probability ≈ {proba:.1%})")
        st.markdown(
            "> The model predicts this patient is **likely diabetic** based on the "
            "provided indicators. A medical check-up (HbA1c / fasting glucose) "
            "is strongly recommended."
        )
    else:
        st.success(f"✅  **Low risk of diabetes**   "
                   f"(probability ≈ {proba:.1%})")
        st.markdown(
            "> The model predicts this patient is **unlikely diabetic** based on the "
            "provided indicators. Maintain a healthy lifestyle for prevention."
        )

    # Probability bar
    st.progress(proba)
    st.caption(f"Confidence breakdown:  No Diabetes {1-proba:.1%}   |   Diabetes {proba:.1%}")


# ----------------------------------------------------------------
# SIDEBAR  —  about the model + dataset
# ----------------------------------------------------------------
with st.sidebar:
    st.title("About this app")
    st.markdown(
        "This app predicts diabetes risk using a **Random Forest classifier** "
        "trained on the **BRFSS 2015** health survey (70k+ patients)."
    )
    st.metric("Test accuracy", f"{metrics['test_accuracy']*100:.2f}%")
    st.metric("Records used",  f"{metrics['test_size']*5:,}")
    st.metric("Features",      metrics["n_features"])

    st.markdown("---")
    st.markdown("**Top 5 risk factors learned**")
    for feat, score in metrics["top_5_features"].items():
        st.markdown(f"- **{feat}**  ·  {score:.3f}")

    st.markdown("---")
    st.caption(
        "Group: Ali Raza, Muhammad Ammar, Taha Ali  ·  Sir Zaki  ·  Sem 2"
    )
    st.caption(
        "⚠️  Educational project only.  Not for medical use."
    )
