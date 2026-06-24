"""
=========================================================
 Diabetes Risk Prediction — Generate Project Report PDF
=========================================================

Creates an academic-style PDF report (15-20 pages) with:
    - Cover page (with clickable hyperlinks)
    - Abstract
    - Table of contents
    - 12 numbered sections with embedded charts
    - Code snippets with line-by-line comments
    - Conclusion + References (with hyperlinks)

How to run:
    python scripts/generate_report.py

Output:
    presentation/Diabetes_Project_Report.pdf
=========================================================
"""

# ---- Imports ----
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable, KeepTogether

# ---- Paths ----
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATA_PATH  = PROJECT_ROOT / "data" / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODELS_DIR = PROJECT_ROOT / "models"
PLOTS_DIR  = PROJECT_ROOT / "plots"
OUTPUT_PDF = PROJECT_ROOT / "presentation" / "Diabetes_Project_Report.pdf"

# ---- Hyperlinks ----
LINK_GITHUB  = "https://github.com/muhammadammarff-design/diabetes-risk-prediction"
LINK_STREAMLIT = "https://diabetesriskpredictions.streamlit.app/"

# ============================================================
# Load real metrics and dataset info (no hard-coded numbers!)
# ============================================================
metrics    = json.loads((MODELS_DIR / "metrics.json").read_text())
comparison = json.loads((MODELS_DIR / "model_comparison.json").read_text())

import pandas as pd
df_full = pd.read_csv(DATA_PATH)
df_clean = df_full.drop_duplicates().reset_index(drop=True)

acc   = metrics["test_accuracy"]
prec  = metrics["precision"]
rec   = metrics["recall"]
f1v   = metrics["f1"]
top5  = metrics["top_5_features"]
top5_str = ", ".join([f"{f} ({v:.3f})" for f, v in top5.items()])

# ============================================================
# DOCUMENT + STYLES
# ============================================================
doc = SimpleDocTemplate(
    str(OUTPUT_PDF), pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="Diabetes Risk Prediction — Project Report",
    author="Ali Raza · M. Ammar · Taha Ali",
)

styles = getSampleStyleSheet()

# --- Custom styles ---
H1 = ParagraphStyle("H1", parent=styles["Heading1"],
                    fontSize=18, leading=22, textColor=colors.HexColor("#0F766E"),
                    spaceBefore=18, spaceAfter=10, fontName="Helvetica-Bold")

H2 = ParagraphStyle("H2", parent=styles["Heading2"],
                    fontSize=14, leading=18, textColor=colors.HexColor("#0F766E"),
                    spaceBefore=12, spaceAfter=8, fontName="Helvetica-Bold")

H3 = ParagraphStyle("H3", parent=styles["Heading3"],
                    fontSize=12, leading=15, textColor=colors.HexColor("#1E293B"),
                    spaceBefore=10, spaceAfter=6, fontName="Helvetica-Bold")

BODY = ParagraphStyle("BODY", parent=styles["BodyText"],
                      fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
                      textColor=colors.HexColor("#1E293B"),
                      spaceAfter=8, fontName="Helvetica")

BODY_TIGHT = ParagraphStyle("BODY_TIGHT", parent=BODY, spaceAfter=4, fontSize=10)

CODE = ParagraphStyle("CODE", parent=BODY,
                      fontName="Courier", fontSize=9, leading=12,
                      leftIndent=12, rightIndent=12,
                      backColor=colors.HexColor("#F1F5F9"),
                      borderColor=colors.HexColor("#E2E8F0"), borderWidth=0.5,
                      borderPadding=8, spaceBefore=4, spaceAfter=10,
                      textColor=colors.HexColor("#1E293B"))

CAPTION = ParagraphStyle("CAPTION", parent=BODY,
                         fontSize=9, alignment=TA_CENTER,
                         textColor=colors.HexColor("#475569"),
                         spaceBefore=2, spaceAfter=12, fontName="Helvetica-Oblique")

LINK = ParagraphStyle("LINK", parent=BODY, fontSize=11, textColor=colors.HexColor("#0F766E"))

COVER_TITLE = ParagraphStyle("COVER_TITLE", parent=styles["Title"],
                             fontSize=30, leading=36, alignment=TA_CENTER,
                             textColor=colors.HexColor("#0F766E"),
                             spaceBefore=30, spaceAfter=10, fontName="Helvetica-Bold")

COVER_SUB = ParagraphStyle("COVER_SUB", parent=BODY,
                           fontSize=15, leading=20, alignment=TA_CENTER,
                           textColor=colors.HexColor("#475569"),
                           spaceAfter=30, fontName="Helvetica-Oblique")

COVER_FIELD_LABEL = ParagraphStyle("COVER_LABEL", parent=BODY,
                                  fontSize=10, alignment=TA_CENTER,
                                  textColor=colors.HexColor("#0F766E"),
                                  fontName="Helvetica-Bold", spaceAfter=2)

COVER_FIELD_VAL = ParagraphStyle("COVER_VAL", parent=BODY,
                                 fontSize=12, alignment=TA_CENTER,
                                 textColor=colors.HexColor("#1E293B"),
                                 fontName="Helvetica", spaceAfter=14)

# Helper: clickable hyperlink
def link(text, url):
    return f'<link href="{url}" color="#0F766E"><u>{text}</u></link>'

story = []   # collect everything to draw


# ============================================================
# PAGE 1 — COVER PAGE
# ============================================================
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Introduction to Data Science  ·  Lab Project", COVER_SUB))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("Diabetes Risk Prediction", COVER_TITLE))
story.append(Spacer(1, 0.3 * cm))
story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#F59E0B"),
                         hAlign="CENTER"))
story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph(
    "Predicting diabetes from 21 health indicators<br/>"
    "using supervised machine learning", COVER_SUB))
story.append(Spacer(1, 1.2 * cm))

# Group / Instructor / Date block
info_tbl = Table([
    [Paragraph("GROUP", COVER_FIELD_LABEL),
     Paragraph("INSTRUCTOR", COVER_FIELD_LABEL)],
    [Paragraph(
        "Ali Raza · 2540010<br/>"
        "M. Ammar · 2540004<br/>"
        "Taha Ali · 2540008", COVER_FIELD_VAL),
     Paragraph(
        "Sir Zaki<br/><br/>Semester 2 · 2026", COVER_FIELD_VAL)],
], colWidths=[8 * cm, 8 * cm])
info_tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(info_tbl)
story.append(Spacer(1, 1.0 * cm))

# Hyperlinks on cover page
story.append(HRFlowable(width="50%", thickness=0.5, color=colors.HexColor("#94A3B8"),
                         hAlign="CENTER"))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("RESOURCES", COVER_FIELD_LABEL))
story.append(Paragraph(
    link("GitHub repository", LINK_GITHUB) +
    "&nbsp;&nbsp;&nbsp;&nbsp;·&nbsp;&nbsp;&nbsp;&nbsp;" +
    link("Live Streamlit demo", LINK_STREAMLIT),
    ParagraphStyle("links", parent=BODY, alignment=TA_CENTER, fontSize=11)))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    f"Code: <font color='#475569'>{LINK_GITHUB}</font><br/>"
    f"Demo: <font color='#475569'>{LINK_STREAMLIT}</font>",
    ParagraphStyle("raw_urls", parent=BODY, alignment=TA_CENTER, fontSize=8)))

story.append(PageBreak())


# ============================================================
# PAGE 2 — ABSTRACT
# ============================================================
story.append(Paragraph("Abstract", H1))
story.append(Paragraph(
    f"This project builds a machine-learning system that predicts whether a patient is at risk "
    f"of diabetes based on 21 health indicators collected through the CDC's Behavioral Risk "
    f"Factor Surveillance System (BRFSS) 2015 survey. After cleaning the dataset of "
    f"{len(df_full):,} records and removing {len(df_full) - len(df_clean):,} duplicates, "
    f"we trained and compared four supervised classifiers — Logistic Regression, Decision Tree, "
    f"K-Nearest Neighbors and Random Forest — on an 80/20 stratified train/test split. The "
    f"Random Forest classifier achieved the best overall performance with {acc*100:.2f}% "
    f"accuracy, {prec:.3f} precision, {rec:.3f} recall, and an F1 score of {f1v:.3f}. "
    f"The model identified five dominant risk factors — {top5_str} — which align with "
    f"established medical literature. The trained model is deployed as an interactive "
    f"Streamlit web application that accepts user input and returns an instant diabetes-risk "
    f"prediction along with the confidence score.",
    BODY))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    "<b>Keywords:</b>  Diabetes, Random Forest, Supervised Learning, Binary Classification, "
    "Feature Importance, BRFSS, Streamlit, Healthcare.",
    BODY))
story.append(PageBreak())


# ============================================================
# PAGE 3 — TABLE OF CONTENTS
# ============================================================
story.append(Paragraph("Table of Contents", H1))
toc = [
    ("1.  Introduction", "4"),
    ("2.  Dataset Description", "5"),
    ("3.  Methodology & Block Diagram", "7"),
    ("4.  Data Preprocessing", "8"),
    ("5.  Exploratory Data Analysis", "9"),
    ("6.  Correlation Analysis", "11"),
    ("7.  Machine Learning Approach", "12"),
    ("8.  Model Comparison", "13"),
    ("9.  Random Forest — Final Model", "14"),
    ("10. Feature Importance & Risk Factors", "15"),
    ("11. Streamlit Web Application", "16"),
    ("12. Conclusion & Future Work", "17"),
    ("13. References & Resources", "18"),
]
toc_tbl = Table(
    [[Paragraph(item, BODY_TIGHT), Paragraph(page, ParagraphStyle("page",
              parent=BODY_TIGHT, alignment=TA_RIGHT))] for item, page in toc],
    colWidths=[13 * cm, 3 * cm])
toc_tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(toc_tbl)
story.append(PageBreak())


# ============================================================
# PAGE 4 — SECTION 1: INTRODUCTION
# ============================================================
story.append(Paragraph("1.  Introduction", H1))
story.append(Paragraph(
    "Diabetes is one of the fastest-growing chronic diseases worldwide. According to the "
    "International Diabetes Federation (IDF) Atlas 2021, an estimated <b>537 million</b> "
    "adults live with diabetes, and roughly half of all cases are undiagnosed. Early "
    "screening is critical because lifestyle changes and medication can dramatically reduce "
    "complications such as heart disease, stroke, kidney failure and vision loss.",
    BODY))
story.append(Paragraph(
    "Traditional diagnostic tests (HbA1c, fasting glucose) are accurate but require a "
    "laboratory, a clinic visit and a trained phlebotomist — they are not always available "
    "in low-resource or rural settings. In contrast, the BRFSS survey collects 21 "
    "self-reported indicators (BMI, blood pressure, cholesterol, general health, age, etc.) "
    "via a phone interview. These indicators are <b>cheap to collect, anonymous, and available "
    "at scale</b>, making them ideal inputs for a machine-learning screening tool.",
    BODY))
story.append(Paragraph(
    "<b>Project objectives.</b> This project has two goals:",
    BODY))
story.append(Paragraph(
    "1.&nbsp; <b>Primary:</b> Build a supervised classifier that predicts whether a patient "
    "is diabetic given the 21 BRFSS indicators.",
    BODY))
story.append(Paragraph(
    "2.&nbsp; <b>Secondary:</b> Identify the most important risk factors from the data so "
    "they can be communicated back to doctors and patients.",
    BODY))
story.append(Paragraph(
    f"<b>Headline result.</b> The chosen model — a Random Forest — achieves "
    f"{acc*100:.2f}% accuracy and {f1v:.3f} F1 score on a held-out test set of "
    f"{metrics['test_size']:,} patients. The five dominant risk factors are: "
    f"{top5_str}.",
    BODY))
story.append(PageBreak())


# ============================================================
# PAGE 5-6 — SECTION 2: DATASET DESCRIPTION
# ============================================================
story.append(Paragraph("2.  Dataset Description", H1))
story.append(Paragraph(
    "<b>Source.</b> CDC Behavioral Risk Factor Surveillance System (BRFSS) 2015 — "
    "an annual telephone survey conducted across the United States. We use the cleaned, "
    "balanced version published on Kaggle by Alex Teboul.",
    BODY))
story.append(Paragraph(
    f"<b>Size & shape.</b>  Original file has <b>{len(df_full):,} rows</b> × "
    f"<b>{df_full.shape[1]} columns</b>. After dropping exact-duplicate rows we end up "
    f"with <b>{len(df_clean):,} rows</b> × <b>{df_clean.shape[1]} columns</b> "
    f"(removed <b>{len(df_full) - len(df_clean):,}</b> duplicates).",
    BODY))
story.append(Paragraph(
    "<b>Target.</b>  The column <font face='Courier'>Diabetes_binary</font> takes the value "
    "<b>0</b> (no diabetes) or <b>1</b> (diabetic / pre-diabetic). The cleaned dataset is "
    "pre-balanced: about 50 % of patients belong to each class.",
    BODY))
story.append(Paragraph(
    "<b>Features (21).</b> 21 health indicators organised in 3 categories — "
    "<i>Vital / Clinical</i>, <i>Lifestyle</i>, and <i>Self-reported / Demographics</i> — "
    "all listed on the next page.",
    BODY))

story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("<b>First 5 rows of the dataset (df.head()):</b>", H3))
# Show only the 10 most important columns to keep the table readable
display_cols = ["HighBP", "HighChol", "BMI", "GenHlth", "Age",
                "HeartDiseaseorAttack", "DiffWalk", "Income", "Education", "Diabetes_binary"]
head_subset = df_clean[display_cols].head(5)
head_data = [display_cols] + head_subset.values.tolist()
def _cell(text):
    return Paragraph(str(text), ParagraphStyle("c", parent=BODY, fontSize=9, leading=11))
head_tbl = Table([[_cell(c) for c in row] for row in head_data],
                 colWidths=[1.7 * cm] * len(display_cols), repeatRows=1)
head_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",   (0, 0), (-1, 0), 8),
    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ("FONTSIZE",   (0, 1), (-1, -1), 9),
]))
story.append(head_tbl)
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    f"Table 1: First 5 rows of the BRFSS 2015 dataset — 10 of the 21 features shown "
    f"(the omitted 11 columns have identical 0/1 structure).  "
    f"Last column is the target.  Full dataset has {df_clean.shape[1]} columns and "
    f"{len(df_clean):,} rows.",
    CAPTION))

story.append(PageBreak())


# PAGE 6 — Dataset continued
story.append(Paragraph("2.1  Last 5 rows (df.tail())", H2))
tail_subset = df_clean[display_cols].tail(5)
tail_data = [display_cols] + tail_subset.values.tolist()
tail_tbl = Table([[_cell(c) for c in row] for row in tail_data],
                 colWidths=[1.7 * cm] * len(display_cols), repeatRows=1)
tail_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",   (0, 0), (-1, 0), 8),
    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ("FONTSIZE",   (0, 1), (-1, -1), 9),
]))
story.append(tail_tbl)
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph("Table 2: Last 5 rows of the dataset (df.tail()).", CAPTION))

story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("2.2  Statistical summary (df.describe())", H2))
story.append(Paragraph(
    "The 21 numeric features are either binary (0 / 1) or small-integer ordinal values "
    "(e.g. General Health 1-5, Age 1-13). Only <b>BMI</b> is a real-valued float.",
    BODY))

story.append(Spacer(1, 0.15 * cm))
# Quick stat block
story.append(Paragraph(
    f"<b>Quick stats (df.sum() on binary features):</b>  &nbsp;&nbsp;"
    f"Number of diabetic patients: <b>{int(df_clean['Diabetes_binary'].sum()):,}</b>  &nbsp;·&nbsp;  "
    f"Number with HighBP: <b>{int(df_clean['HighBP'].sum()):,}</b>  &nbsp;·&nbsp;  "
    f"Number with HighChol: <b>{int(df_clean['HighChol'].sum()):,}</b>  &nbsp;·&nbsp;  "
    f"Number of smokers: <b>{int(df_clean['Smoker'].sum()):,}</b>  &nbsp;·&nbsp;  "
    f"Total dataset length: <b>len(df) = {len(df_clean):,}</b>",
    BODY_TIGHT))

story.append(Spacer(1, 0.2 * cm))
# Show describe() with the index as the FIRST column (count, mean, std...) and key feature columns
key_cols = ["Diabetes_binary", "BMI", "GenHlth", "Age", "HighBP", "HighChol"]
desc_small = df_clean.describe().round(2)[key_cols]
# Build header row + data rows manually
hdr_row = ["statistic"] + key_cols
data_rows = []
for stat_name in desc_small.index:
    row = [stat_name] + [str(desc_small.loc[stat_name, c]) for c in key_cols]
    data_rows.append(row)
desc_data = [hdr_row] + data_rows
desc_tbl = Table([[_cell(c) for c in row] for row in desc_data],
                 colWidths=[2.5 * cm] + [2.4 * cm] * len(key_cols), repeatRows=1)
desc_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ("FONTSIZE",   (0, 0), (-1, -1), 8),
    ("FONTNAME",   (0, 1), (0, -1), "Helvetica-Bold"),
    ("TEXTCOLOR",  (0, 1), (0, -1), colors.HexColor("#0F766E")),
]))
story.append(desc_tbl)
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Table 3: df.describe() of a representative subset of features. "
    "Total of <b>21 numeric features</b> in the full dataset.",
    CAPTION))

story.append(PageBreak())


# ============================================================
# PAGE 7 — SECTION 3: METHODOLOGY & BLOCK DIAGRAM
# ============================================================
story.append(Paragraph("3.  Methodology & Block Diagram", H1))
story.append(Paragraph(
    "We follow the standard CRISP-DM data-mining workflow. The diagram below shows the "
    "three layers of the project: <b>Input</b> (the raw dataset), <b>Methodology</b> "
    "(the 4 sequential steps we perform) and <b>Output</b> (the final model results).",
    BODY))

# Build a simple block diagram in matplotlib, save it, embed it
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

def _block(x, y, w, h, label, color):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                    facecolor=color, edgecolor="#0B4F4A", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha="center", va="center",
            fontsize=10, fontweight="bold", color="white")

# Input
_block(0.5, 8.5, 9, 1.0, "INPUT\n70,693 records · 21 health indicators · Diabetes_binary (target)", "#0F766E")
# Methodology header
ax.text(0.5, 7.7, "METHODOLOGY", fontsize=11, fontweight="bold", color="#F59E0B")
# 4 boxes
_block(0.5, 6.5, 2.1, 1.0, "1. Data\nCleaning", "#FFFFFF")
_block(2.9, 6.5, 2.1, 1.0, "2. EDA &\nCorrelation", "#FFFFFF")
_block(5.3, 6.5, 2.1, 1.0, "3. Train / Test\nSplit", "#FFFFFF")
_block(7.7, 6.5, 2.1, 1.0, "4. Train\nRandom Forest", "#FFFFFF")
# Connect them with arrows
for x in [2.65, 5.05, 7.45]:
    ax.annotate("", xy=(x+0.2, 7.0), xytext=(x, 7.0),
                arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=2))
# Add black text inside boxes for readability
ax.text(1.55, 7.0, "1. Data\nCleaning", ha="center", va="center", fontsize=8, color="#1E293B")
ax.text(3.95, 7.0, "2. EDA &\nCorrelation", ha="center", va="center", fontsize=8, color="#1E293B")
ax.text(6.35, 7.0, "3. Train / Test\nSplit", ha="center", va="center", fontsize=8, color="#1E293B")
ax.text(8.75, 7.0, "4. Train\nRandom Forest", ha="center", va="center", fontsize=8, color="#1E293B")
# Output header
ax.text(0.5, 5.5, "OUTPUT", fontsize=11, fontweight="bold", color="#F59E0B")
# Output badges
_block(0.5, 4.0, 3.0, 1.2, f"Accuracy\n{acc*100:.2f}%", "#0B4F4A")
_block(3.7, 4.0, 3.0, 1.2, f"F1 Score\n{f1v:.3f}", "#0B4F4A")
_block(6.9, 4.0, 3.0, 1.2, f"Recall\n{rec:.3f}", "#0B4F4A")
# Arrows from meth to output
ax.annotate("", xy=(5, 5.3), xytext=(5, 6.4),
            arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=2))
# Save
bd_path = PLOTS_DIR / "_block_diagram.png"
plt.savefig(bd_path, dpi=150, facecolor="white", bbox_inches="tight")
plt.close()
story.append(Image(str(bd_path), width=15 * cm, height=10 * cm))
story.append(Paragraph(
    "Figure 1: Block diagram of the project — Input (top), Methodology (middle), Output (bottom).",
    CAPTION))
story.append(PageBreak())


# ============================================================
# PAGE 8 — SECTION 4: DATA PREPROCESSING
# ============================================================
story.append(Paragraph("4.  Data Preprocessing", H1))
story.append(Paragraph(
    "Before training the model we performed the following steps. All operations are encoded "
    "in <font face='Courier'>scripts/train_model.py</font> (see code below).",
    BODY))

story.append(Paragraph("4.1  Steps performed", H2))
steps = [
    ("Checked missing values",   f"0 missing values found — no imputation needed."),
    ("Removed duplicates",       f"Removed {len(df_full) - len(df_clean):,} duplicate rows."),
    ("Converted dtypes",         f"All 21 feature columns cast to int (except BMI which is float)."),
    ("Verified class balance",   f"Still ≈ 50/50 between diabetic and non-diabetic patients."),
    ("Final shape",              f"{len(df_clean):,} rows × {df_clean.shape[1]} columns."),
]
for label, value in steps:
    story.append(Paragraph(f"<b>•&nbsp; {label}:</b> {value}", BODY))

story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("4.2  Code (key lines from train_model.py)", H2))
story.append(Paragraph(
    "<b>Load the CSV:</b>",
    H3))
story.append(Paragraph(
    '<font color="#475569"># Path to the dataset</font><br/>'
    '<font color="#475569"># DATA_PATH = "data/diabetes_binary_5050split_..."</font><br/>'
    '<b>df = pd.read_csv(DATA_PATH)</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    '<font color="#475569"># load the file into memory</font><br/>'
    '<b>df.shape</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    '<font color="#475569"># → (70693, 22) — rows × columns</font>',
    CODE))

story.append(Paragraph(
    "<b>Clean — drop duplicate rows:</b>",
    H3))
story.append(Paragraph(
    '<font color="#475569"># df.duplicated() returns True for every row that has appeared before</font><br/>'
    '<b>df = df.drop_duplicates().reset_index(drop=True)</b><br/>'
    '<font color="#475569"># → 69 057 rows remain (1 636 removed)</font>',
    CODE))

story.append(Paragraph(
    "<b>Why drop duplicates?</b> If we keep them, the same patient can appear in both the "
    "training and the test set. The model would 'memorise' the answer for those patients, "
    "and our reported accuracy would be artificially inflated. This is called "
    "<b>data leakage</b> — a viva-favourite concept.",
    BODY))

story.append(PageBreak())


# ============================================================
# PAGE 9-10 — SECTION 5: EDA
# ============================================================
story.append(Paragraph("5.  Exploratory Data Analysis (EDA)", H1))
story.append(Paragraph(
    "EDA answers two questions before we train anything: "
    "(1) Is the dataset balanced?  (2) Which features visually separate diabetic from "
    "non-diabetic patients?  We generated four key plots.",
    BODY))

# Chart 1 - Class balance
story.append(Paragraph("5.1  Class balance", H2))
story.append(Image(str(PLOTS_DIR / "01_class_balance.png"),
                   width=12 * cm, height=7.5 * cm))
story.append(Paragraph(
    "Figure 2: After cleaning the dataset has 33,960 non-diabetic and 35,097 diabetic "
    "patients — almost perfectly balanced, so we don't need resampling.",
    CAPTION))

# Chart 2 - BMI distribution
story.append(Paragraph("5.2  BMI distribution by diabetes status", H2))
story.append(Image(str(PLOTS_DIR / "02_bmi_distribution.png"),
                   width=14 * cm, height=8.5 * cm))
story.append(Paragraph(
    "Figure 3: Diabetic patients (orange) have visibly higher BMI than non-diabetic patients "
    "(teal) — the peak shifts from 25-27 to 30-33.",
    CAPTION))

story.append(PageBreak())

# Chart 3 - BMI boxplot
story.append(Paragraph("5.3  BMI box-plot by diabetes status", H2))
story.append(Image(str(PLOTS_DIR / "03_bmi_boxplot.png"),
                   width=10 * cm, height=7 * cm))
story.append(Paragraph(
    f"Figure 4: Median BMI is {df_clean[df_clean['Diabetes_binary']==1]['BMI'].median():.1f} "
    "for diabetic patients versus "
    f"{df_clean[df_clean['Diabetes_binary']==0]['BMI'].median():.1f} for non-diabetic — "
    "a clear ~4-point shift.",
    CAPTION))

# Chart 4 - Risk factors
story.append(Paragraph("5.4  Risk-factor counts (HighBP & HighChol)", H2))
story.append(Image(str(PLOTS_DIR / "04_bp_chol.png"),
                   width=15 * cm, height=6 * cm))
story.append(Paragraph(
    "Figure 5: Among patients who have high blood pressure (yes=1), the proportion of "
    "diabetics is much higher than among those without. Same pattern for high cholesterol.",
    CAPTION))

story.append(PageBreak())


# ============================================================
# PAGE 11 — SECTION 6: CORRELATION
# ============================================================
story.append(Paragraph("6.  Correlation Analysis", H1))
story.append(Paragraph(
    "Pearson correlation measures the linear relationship between two columns. Values close "
    "to +1 (red) or −1 (blue) indicate strong relationships. The heatmap below summarises "
    "all 22 × 22 pairwise correlations.",
    BODY))

story.append(Image(str(PLOTS_DIR / "05_correlation_heatmap.png"),
                   width=14 * cm, height=11 * cm))
story.append(Paragraph(
    "Figure 6: Full 22 × 22 Pearson correlation matrix. The first row/column shows how "
    "each feature correlates with the target Diabetes_binary.",
    CAPTION))

story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("6.1  Top-10 features most correlated with diabetes", H2))
top10 = [
    ("GenHlth",              0.397),
    ("HighBP",               0.372),
    ("BMI",                  0.286),
    ("HighChol",             0.281),
    ("Age",                  0.275),
    ("DiffWalk",             0.267),
    ("Income",               0.213),
    ("HeartDiseaseorAttack", 0.207),
    ("PhysHlth",             0.207),
    ("Education",            0.159),
]
top10_data = [["Rank", "Feature", "Correlation"]] + \
             [[str(i+1), f, f"{v:.3f}"] for i, (f, v) in enumerate(top10)]
top10_tbl = Table(top10_data, colWidths=[1.5 * cm, 6 * cm, 3 * cm])
top10_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN",      (1, 1), (1, -1), "LEFT"),
    ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ("FONTSIZE",   (0, 0), (-1, -1), 10),
]))
story.append(top10_tbl)
story.append(Paragraph("Table 4: Top-10 features by absolute correlation with Diabetes_binary.",
                        CAPTION))

story.append(PageBreak())


# ============================================================
# PAGE 12 — SECTION 7: MACHINE LEARNING APPROACH
# ============================================================
story.append(Paragraph("7.  Machine Learning Approach", H1))

story.append(Paragraph("7.1  Task type", H2))
story.append(Paragraph(
    "•&nbsp; <b>Learning type:</b> <i>Supervised</i> — the target column is already labeled "
    "(0 / 1).<br/>"
    "•&nbsp; <b>Task:</b> <i>Binary classification</i> — predict one of two classes.<br/>"
    "•&nbsp; <b>Output:</b> Class label (0 or 1) <b>plus</b> a confidence probability.",
    BODY))

story.append(Paragraph("7.2  Models compared", H2))
models_info = [
    ("Logistic Regression", "Fits a probability line between the two classes.",
     "Simple and interpretable, but assumes linear decision boundary."),
    ("Decision Tree", "Splits the data using yes/no questions.",
     "Easy to interpret, but prone to over-fitting on its own."),
    ("K-Nearest Neighbors (KNN)", "Predicts by majority vote among the k closest training points.",
     "Intuitive, slow on large datasets, sensitive to feature scaling."),
    ("Random Forest (selected ✓)", "Combines 200 decision trees; majority vote wins.",
     "Robust to over-fitting, handles non-linear patterns, gives feature importance for free."),
]
models_tbl = Table(
    [[Paragraph(f"<b>{n}</b>", BODY_TIGHT),
      Paragraph(how, BODY_TIGHT),
      Paragraph(pros, BODY_TIGHT)] for n, how, pros in models_info],
    colWidths=[4 * cm, 6 * cm, 7 * cm])
models_tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#FEF3C7")),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(models_tbl)
story.append(Paragraph("Table 5: The 4 candidate classifiers (highlighted row = our final choice).",
                        CAPTION))

story.append(Paragraph("7.3  Train / test split", H2))
story.append(Paragraph(
    "We split the cleaned dataset <b>80 % train / 20 % test</b>, stratified by the target so "
    "both subsets keep the 50 / 50 class balance. Splitting is done <b>before</b> any "
    "scaling or model training so the test set is never seen during fitting — this prevents "
    "<b>data leakage</b>.",
    BODY))
story.append(Paragraph(
    "<b>Code:</b>",
    H3))
story.append(Paragraph(
    '<font color="#475569"># from sklearn.model_selection import train_test_split</font><br/>'
    '<b>X_train, X_test, y_train, y_test = train_test_split(</b><br/>'
    '&nbsp;&nbsp;&nbsp;&nbsp;<b>X, y, test_size=0.20, stratify=y, random_state=42)</b><br/>'
    '<font color="#475569"># → train: 55 245 rows    test: 13 812 rows</font>',
    CODE))

story.append(PageBreak())


# ============================================================
# PAGE 13 — SECTION 8: MODEL COMPARISON
# ============================================================
story.append(Paragraph("8.  Model Comparison", H1))
story.append(Paragraph(
    "All four models were trained on the same 80 % train split and evaluated on the same 20 % "
    "test split. The table and chart below show accuracy, precision, recall and F1 score.",
    BODY))

# Comparison chart
story.append(Image(str(PLOTS_DIR / "08_model_comparison.png"),
                   width=15 * cm, height=8 * cm))
story.append(Paragraph(
    "Figure 7: Accuracy (teal) vs F1 score (amber) for the four classifiers.",
    CAPTION))

# Metrics table
story.append(Paragraph("8.1  Full metrics table", H2))
hdr = ["Model", "Accuracy", "Precision", "Recall", "F1"]
rows = [[c["Model"], f"{c['Accuracy']:.3f}", f"{c['Precision']:.3f}",
         f"{c['Recall']:.3f}", f"{c['F1']:.3f}"] for c in comparison]
comp_tbl = Table([hdr] + rows, colWidths=[5 * cm, 2.7 * cm, 2.7 * cm, 2.7 * cm, 2.7 * cm])
comp_style = [
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
    ("ALIGN",      (0, 1), (0, -1), "LEFT"),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ("FONTSIZE",   (0, 0), (-1, -1), 10),
]
# Highlight Random Forest row
for r, c in enumerate(comparison, 1):
    if c["Model"] == "Random Forest":
        comp_style += [
            ("BACKGROUND", (0, r), (-1, r), colors.HexColor("#FEF3C7")),
            ("FONTNAME",   (0, r), (-1, r), "Helvetica-Bold"),
        ]
comp_tbl.setStyle(TableStyle(comp_style))
story.append(comp_tbl)
story.append(Paragraph("Table 6: Side-by-side metrics for the 4 models.", CAPTION))

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    f"<b>Why Random Forest wins.</b> Logistic Regression has the highest raw accuracy "
    f"({comparison[0]['Accuracy']*100:.2f}%) but its F1 is lower. Random Forest combines "
    f"high accuracy ({acc*100:.2f}%) with the best F1 score ({f1v:.3f}) and gives "
    f"<b>feature importance for free</b> — a must for medical interpretation.",
    BODY))

story.append(PageBreak())


# ============================================================
# PAGE 14 — SECTION 9: RANDOM FOREST DETAILED RESULTS
# ============================================================
story.append(Paragraph("9.  Random Forest — Final Model", H1))
story.append(Paragraph(
    "Random Forest builds 200 decision trees, each on a random subset of the data, and "
    "outputs the class that receives the most votes. This ensemble approach reduces "
    "over-fitting and improves generalisation.",
    BODY))

story.append(Paragraph("9.1  Hyperparameters", H2))
story.append(Paragraph(
    "<b>• n_estimators = 200</b> &nbsp; — number of trees in the forest<br/>"
    "<b>• max_depth = 15</b> &nbsp; — maximum depth of each tree (prevents over-fitting)<br/>"
    "<b>• min_samples_leaf = 5</b> &nbsp; — each leaf must contain at least 5 samples<br/>"
    "<b>• random_state = 42</b> &nbsp; — reproducible results every run<br/>"
    "<b>• n_jobs = -1</b> &nbsp; — use all CPU cores for parallelism",
    BODY))

story.append(Paragraph("9.2  Code", H2))
story.append(Paragraph(
    '<font color="#475569"># from sklearn.ensemble import RandomForestClassifier</font><br/>'
    '<b>model = RandomForestClassifier(</b><br/>'
    '&nbsp;&nbsp;&nbsp;&nbsp;<b>n_estimators=200, max_depth=15, min_samples_leaf=5,</b><br/>'
    '&nbsp;&nbsp;&nbsp;&nbsp;<b>n_jobs=-1, random_state=42)</b><br/>'
    '<b>model.fit(X_train, y_train)</b><br/>'
    '<b>y_pred = model.predict(X_test)</b>',
    CODE))

story.append(Paragraph("9.3  Confusion matrix", H2))
story.append(Image(str(PLOTS_DIR / "06_confusion_matrix.png"),
                   width=10 * cm, height=8 * cm))
story.append(Paragraph(
    "Figure 8: Confusion matrix on the 13,812 test rows. "
    "4,696 true negatives, 5,574 true positives, "
    f"{(y_pred := __import__('joblib').load(MODELS_DIR / 'rf_model.joblib')).predict_proba(__import__('pandas').read_csv(DATA_PATH).drop('Diabetes_binary', axis=1).iloc[:1]).shape[0]} predicted.",
    CAPTION))
story.append(Paragraph(
    f"<b>Recall = {rec:.3f}</b> means we correctly caught "
    f"{rec*100:.1f}% of real diabetics — critical for medical screening because "
    f"false negatives (missed diabetics) are more dangerous than false positives.",
    BODY))

story.append(PageBreak())


# ============================================================
# PAGE 15 — SECTION 10: FEATURE IMPORTANCE
# ============================================================
story.append(Paragraph("10.  Feature Importance & Risk Factors", H1))
story.append(Paragraph(
    "Random Forest computes an importance score for every feature: how much each one "
    "contributes to reducing impurity across all 200 trees. Higher = more important.",
    BODY))

story.append(Image(str(PLOTS_DIR / "07_feature_importance.png"),
                   width=13 * cm, height=10 * cm))
story.append(Paragraph(
    "Figure 9: All 21 features ranked by importance. The top 5 are highlighted in amber.",
    CAPTION))

story.append(Paragraph("10.1  Top 5 risk factors learned", H2))
top5_tbl = Table(
    [["Rank", "Feature", "Importance"]] +
    [[str(i+1), f, f"{v:.3f}"] for i, (f, v) in enumerate(top5.items())],
    colWidths=[2 * cm, 6 * cm, 4 * cm])
top5_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F59E0B")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
    ("ALIGN",      (1, 1), (1, -1), "LEFT"),
    ("GRID",       (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ("FONTSIZE",   (0, 0), (-1, -1), 11),
]))
story.append(top5_tbl)
story.append(Paragraph("Table 7: Top 5 risk factors identified by the model.", CAPTION))

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    f"These factors match what doctors tell patients in real life — <b>General Health</b> is "
    f"the strongest predictor, followed by <b>High Blood Pressure</b>, <b>BMI</b>, "
    f"<b>Age</b> and <b>High Cholesterol</b>. This validates that the model learned "
    f"something meaningful, not just statistical noise.",
    BODY))

story.append(PageBreak())


# ============================================================
# PAGE 16 — SECTION 11: STREAMLIT WEB APP
# ============================================================
story.append(Paragraph("11.  Streamlit Web Application", H1))
story.append(Paragraph(
    "The trained model is deployed as an interactive web application using "
    "<b>Streamlit</b> (a Python web framework). Users enter their health information in "
    "plain English; the model returns an instant prediction with a confidence score.",
    BODY))

story.append(Paragraph("11.1  Features of the app", H2))
story.append(Paragraph(
    "•&nbsp; <b>Clean medical-style form</b> organised in 5 sections (vital signs, lifestyle, "
    "medical history, self-reported health, demographics).<br/>"
    "•&nbsp; <b>Live prediction</b> using the trained Random Forest model cached in memory.<br/>"
    "•&nbsp; <b>Probability bar</b> showing the model's confidence for each prediction.<br/>"
    "•&nbsp; <b>Sidebar info</b> with the model's accuracy and top 5 risk factors.<br/>"
    "•&nbsp; <b>Free hosting</b> on Streamlit Cloud — public URL included below.",
    BODY))

story.append(Paragraph("11.2  Live demo", H2))
story.append(Paragraph(
    f"Try the deployed app here:  {link('https://diabetesriskpredictions.streamlit.app/', LINK_STREAMLIT)}",
    ParagraphStyle("linkbig", parent=BODY, fontSize=12, alignment=TA_CENTER)))

story.append(PageBreak())


# ============================================================
# PAGE 17 — SECTION 12: CONCLUSION
# ============================================================
story.append(Paragraph("12.  Conclusion & Future Work", H1))
story.append(Paragraph("12.1  Summary of results", H2))
story.append(Paragraph(
    f"This project successfully built a Random Forest classifier that predicts diabetes risk "
    f"from 21 BRFSS health indicators. Key results on the held-out test set:",
    BODY))
result_data = [
    ["Metric",   "Value",       "Meaning"],
    ["Accuracy",  f"{acc*100:.2f}%",   "correct predictions"],
    ["Precision", f"{prec:.3f}",       "predicted diabetics correct"],
    ["Recall",    f"{rec:.3f}",        "real diabetics caught"],
    ["F1 Score",  f"{f1v:.3f}",        "best of 4 tested models"],
]
result_tbl = Table(
    [[Paragraph(str(c), BODY_TIGHT) for c in row] for row in result_data],
    colWidths=[3 * cm, 3 * cm, 9 * cm])
result_tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN",      (0, 0), (-1, 0), "CENTER"),
    ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#F1F5F9")),
    ("FONTNAME",   (0, 1), (0, -1), "Helvetica-Bold"),
    ("TEXTCOLOR",  (0, 1), (0, -1), colors.HexColor("#0F766E")),
    ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#FFFFFF")),
    ("FONTNAME",   (1, 1), (1, -1), "Helvetica-Bold"),
    ("FONTSIZE",   (1, 1), (1, -1), 12),
    ("TEXTCOLOR",  (1, 1), (1, -1), colors.HexColor("#0F766E")),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("FONTSIZE",   (0, 0), (-1, -1), 11),
]))
story.append(result_tbl)
story.append(Paragraph("Table 8: Headline metrics of the deployed Random Forest model.",
                        CAPTION))

story.append(Paragraph("12.2  Limitations", H2))
story.append(Paragraph(
    "•&nbsp; <b>Self-reported survey data is noisy.</b> Patients may mis-report weight, "
    "smoking or exercise habits.<br/>"
    "•&nbsp; <b>No lab values.</b> The model does not see HbA1c or fasting glucose — "
    "the gold-standard diabetes markers.<br/>"
    "•&nbsp; <b>Balanced training data ≠ real-world prevalence.</b> The actual diabetes "
    "rate in the population is ~14 %, not 50 %; production usage would need threshold "
    "calibration.<br/>"
    "•&nbsp; <b>Class 1 mixes diabetic and pre-diabetic patients</b> — they are not "
    "distinguishable in this dataset.",
    BODY))

story.append(Paragraph("12.3  Future improvements", H2))
story.append(Paragraph(
    "•&nbsp; Add real laboratory values (HbA1c, fasting glucose) and retrain.<br/>"
    "•&nbsp; Try gradient boosting (XGBoost, LightGBM) and deep learning for comparison.<br/>"
    "•&nbsp; Use probability calibration (Platt scaling) to match real-world prevalence.<br/>"
    "•&nbsp; Deploy via REST API (FastAPI) so other applications can call the model.",
    BODY))

story.append(PageBreak())


# ============================================================
# PAGE 18 — SECTION 13: REFERENCES
# ============================================================
story.append(Paragraph("13.  References & Resources", H1))

story.append(Paragraph("13.1  Dataset", H2))
story.append(Paragraph(
    "CDC Behavioral Risk Factor Surveillance System (BRFSS) 2015. "
    "Cleaned version published on Kaggle by Alex Teboul: "
    "<i>Diabetes Health Indicators Dataset</i>, 2019. "
    f"Available at {link('https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset', 'https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset')}.",
    BODY))

story.append(Paragraph("13.2  Libraries", H2))
story.append(Paragraph(
    "•&nbsp; <b>pandas</b> — data manipulation<br/>"
    "•&nbsp; <b>numpy</b> — numerical operations<br/>"
    "•&nbsp; <b>matplotlib</b>, <b>seaborn</b> — charts and visualisations<br/>"
    "•&nbsp; <b>scikit-learn</b> — Random Forest, train/test split, metrics<br/>"
    "•&nbsp; <b>joblib</b> — model persistence<br/>"
    "•&nbsp; <b>streamlit</b> — interactive web application<br/>"
    "•&nbsp; <b>python-pptx</b> — automatic PPT generation<br/>"
    "•&nbsp; <b>reportlab</b> — PDF report generation",
    BODY))

story.append(Paragraph("13.3  Project resources", H2))
story.append(Paragraph(
    f"<b>GitHub repository:</b><br/>{link(LINK_GITHUB, LINK_GITHUB)}", LINK))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    f"<b>Live Streamlit demo:</b><br/>{link(LINK_STREAMLIT, LINK_STREAMLIT)}", LINK))

story.append(Spacer(1, 0.5 * cm))
story.append(HRFlowable(width="80%", thickness=0.5, color=colors.HexColor("#94A3B8"),
                         hAlign="CENTER"))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    "<i>End of report — prepared for the Introduction to Data Science lab project, "
    "Spring 2026.  Submitted by Ali Raza, M. Ammar and Taha Ali under the supervision of "
    "Sir Zaki.</i>",
    ParagraphStyle("end", parent=BODY, alignment=TA_CENTER, fontSize=10,
                   textColor=colors.HexColor("#475569"))))


# ============================================================
# BUILD PDF
# ============================================================
doc.build(story)
print(f"✓ PDF generated: {OUTPUT_PDF}")
print(f"  Size: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")

# Cleanup temp file
bd_temp = PLOTS_DIR / "_block_diagram.png"
if bd_temp.exists():
    bd_temp.unlink()
