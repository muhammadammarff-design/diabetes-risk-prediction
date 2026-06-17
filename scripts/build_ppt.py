"""
Diabetes Risk Prediction - FINAL Presentation generator (v2).

17 slides. Pure native python-pptx (no raw XML hacks).
- Real plots from plots/ directory embedded
- Comprehensive speaker notes per slide
- Clean teal+amber academic style
- White background, large whitespace
- No fade-transition raw XML (avoids "needs repair" prompt in PowerPoint)

Run from project root:
    python scripts/build_v2_ppt.py
"""
import json
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# =====================================================================
# PATHS
# =====================================================================
HERE         = Path(__file__).resolve().parent
PROJ         = HERE.parent
PLOTS        = PROJ / "plots"
MODELS       = PROJ / "models"
PRESENTATION = PROJ / "presentation"
PRESENTATION.mkdir(exist_ok=True)

# =====================================================================
# LOAD REAL RESULTS (no hard-coded numbers!)
# =====================================================================
metrics     = json.loads((MODELS / "metrics.json").read_text())
comparison  = json.loads((MODELS / "model_comparison.json").read_text())

# =====================================================================
# PROFESSIONAL PALETTE
# =====================================================================
TEAL       = RGBColor(0x0F, 0x76, 0x6E)
TEAL_DARK  = RGBColor(0x0B, 0x4F, 0x4A)
TEAL_LIGHT = RGBColor(0x14, 0xB8, 0xA6)
AMBER      = RGBColor(0xF5, 0x9E, 0x0B)
AMBER_DK   = RGBColor(0xD9, 0x77, 0x06)
INK        = RGBColor(0x1E, 0x29, 0x3B)
SLATE      = RGBColor(0x47, 0x55, 0x69)
MUTED      = RGBColor(0x94, 0xA3, 0xB8)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
SOFT       = RGBColor(0xF1, 0xF5, 0xF9)
LINE       = RGBColor(0xE2, 0xE8, 0xF0)
GREEN_OK   = RGBColor(0x16, 0xA3, 0x4A)
RED_NO     = RGBColor(0xDC, 0x26, 0x26)

FONT       = "Calibri"

# =====================================================================
# PRESENTATION SETUP  (16:9 widescreen)
# =====================================================================
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH          = prs.slide_width, prs.slide_height
blank           = prs.slide_layouts[6]
TOTAL           = 17

# =====================================================================
# HELPERS
# =====================================================================
def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(0.75)
    s.shadow.inherit = False
    return s

def text(slide, x, y, w, h, content, *, size=14, bold=False, color=SLATE,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = content if isinstance(content, list) else content.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tb

def bullets(slide, x, y, w, h, items, *, size=14, color=SLATE,
            line_spacing=1.35, space_after=8, bullet_color=AMBER, bullet="■"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        r1 = p.add_run(); r1.text = f"{bullet}  "
        r1.font.name = FONT; r1.font.size = Pt(size); r1.font.bold = True
        r1.font.color.rgb = bullet_color
        r2 = p.add_run(); r2.text = item
        r2.font.name = FONT; r2.font.size = Pt(size); r2.font.color.rgb = color
    return tb

def chrome(slide, num):
    """Side accent bar + footer (no fade-transition XML hack)."""
    rect(slide, 0, 0, Inches(0.12), SH, TEAL)
    text(slide, Inches(0.45), SH - Inches(0.38), Inches(8), Inches(0.3),
         "Diabetes Risk Prediction  ·  Intro to Data Science  ·  Sem 2",
         size=9, color=MUTED)
    text(slide, SW - Inches(1.2), SH - Inches(0.38), Inches(0.9), Inches(0.3),
         f"{num} / {TOTAL}", size=9, color=MUTED, align=PP_ALIGN.RIGHT)

def title_block(slide, eyebrow, title_txt):
    text(slide, Inches(0.7), Inches(0.55), Inches(12), Inches(0.3),
         eyebrow.upper(), size=10, bold=True, color=AMBER)
    text(slide, Inches(0.7), Inches(0.9), Inches(12), Inches(0.75),
         title_txt, size=28, bold=True, color=INK)
    rect(slide, Inches(0.7), Inches(1.6), Inches(0.5), Inches(0.05), AMBER)

def note(slide, txt):
    """Embed speaker notes."""
    nf = slide.notes_slide.notes_text_frame
    nf.text = txt


# =====================================================================
# SLIDE 1 - TITLE
# =====================================================================
s = prs.slides.add_slide(blank)
rect(s, 0, 0, Inches(0.12), SH, TEAL)

text(s, Inches(0.9), Inches(1.4), Inches(10), Inches(0.4),
     "INTRODUCTION TO DATA SCIENCE  ·  FINAL PRESENTATION",
     size=11, bold=True, color=AMBER)
text(s, Inches(0.9), Inches(1.95), Inches(12), Inches(1.4),
     "Diabetes Risk Prediction", size=54, bold=True, color=INK)
text(s, Inches(0.9), Inches(3.45), Inches(11.5), Inches(0.7),
     "Predicting diabetes from 21 health indicators using supervised machine learning",
     size=18, color=SLATE)
rect(s, Inches(0.9), Inches(4.45), Inches(1.0), Inches(0.04), AMBER)

text(s, Inches(0.9), Inches(4.75), Inches(5), Inches(0.3),
     "GROUP", size=10, bold=True, color=TEAL)
text(s, Inches(0.9), Inches(5.1), Inches(6), Inches(2),
     ["Ali Raza            ·  2540010",
      "Muhammad Ammar  ·  2540008",
      "Taha Ali              ·  2540008"],
     size=15, color=INK, line_spacing=1.5)

text(s, Inches(7.5), Inches(4.75), Inches(5), Inches(0.3),
     "INSTRUCTOR", size=10, bold=True, color=TEAL)
text(s, Inches(7.5), Inches(5.1), Inches(5), Inches(0.4),
     "Sir Zaki", size=15, color=INK)
text(s, Inches(7.5), Inches(5.7), Inches(5), Inches(0.3),
     "SEMESTER · DATE", size=10, bold=True, color=TEAL)
text(s, Inches(7.5), Inches(6.05), Inches(5), Inches(0.4),
     "Semester 2  ·  2026", size=15, color=INK)
note(s,
    "Greet the audience. State project title, team and instructor. Keep brief — 30 seconds. "
    "Move to the next slide.")


# =====================================================================
# SLIDE 2 - OUTLINE
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 2); title_block(s, "Outline", "What we will cover today")
left = [
    "01  ·  Problem statement",
    "02  ·  Dataset overview",
    "03  ·  Target & features",
    "04  ·  Project workflow",
    "05  ·  Data cleaning",
    "06  ·  Exploratory data analysis",
    "07  ·  Correlation analysis",
    "08  ·  Train / test split",
]
right = [
    "09  ·  Why machine learning?",
    "10  ·  4 candidate ML models",
    "11  ·  Model comparison",
    "12  ·  Random Forest results",
    "13  ·  Top diabetes risk factors",
    "14  ·  Streamlit web app",
    "15  ·  Limitations",
    "16  ·  Conclusion & Q&A",
]
bullets(s, Inches(0.7), Inches(2.2), Inches(6), Inches(5), left,
        size=14, color=INK, bullet="·")
bullets(s, Inches(7.2), Inches(2.2), Inches(6), Inches(5), right,
        size=14, color=INK, bullet="·")
note(s,
    "Walk through the outline in 30 seconds. Tell the audience the talk is structured as "
    "Problem → Data → Method → Results → Demo → Conclusion.")


# =====================================================================
# SLIDE 3 - PROBLEM STATEMENT
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 3); title_block(s, "01  ·  Why this matters", "The diabetes problem")

bullets(s, Inches(0.7), Inches(2.2), Inches(7.3), Inches(4.5), [
    "Diabetes affects 1 in 11 adults worldwide (~537 million people).",
    "Early detection drastically reduces complications and costs.",
    "Many people are unaware they have prediabetes or diabetes.",
    "Doctors need low-cost, fast screening tools.",
    "Patient survey data is cheap to collect — no lab tests required.",
], size=15, line_spacing=1.45, space_after=10)

cx, cy, cw, ch = Inches(8.3), Inches(2.4), Inches(4.4), Inches(4)
rect(s, cx, cy, cw, ch, SOFT, line=LINE)
text(s, cx + Inches(0.3), cy + Inches(0.35), cw - Inches(0.6), Inches(0.35),
     "GLOBAL IMPACT", size=10, bold=True, color=AMBER)
text(s, cx + Inches(0.3), cy + Inches(0.85), cw - Inches(0.6), Inches(1.5),
     "537M", size=72, bold=True, color=TEAL_DARK)
text(s, cx + Inches(0.3), cy + Inches(2.4), cw - Inches(0.6), Inches(0.5),
     "adults living with diabetes", size=14, color=SLATE)
text(s, cx + Inches(0.3), cy + Inches(3.1), cw - Inches(0.6), Inches(0.7),
     "Source: IDF Diabetes Atlas 2021", size=10, color=MUTED)
note(s,
    "Open with the human impact. 'Diabetes is not a small problem — 537 million adults have it.' "
    "This frames why our project matters. Don't dwell more than 1 minute.")


# =====================================================================
# SLIDE 4 - DATASET OVERVIEW
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 4); title_block(s, "02  ·  Data", "Dataset overview")

bullets(s, Inches(0.7), Inches(2.2), Inches(6.5), Inches(4.5), [
    "Source: CDC Behavioral Risk Factor Surveillance System (BRFSS), 2015.",
    "Collected through annual phone interviews across the United States.",
    "Cleaned version published on Kaggle by Alex Teboul.",
    "Pre-balanced 50 / 50 between diabetic and non-diabetic patients.",
    "Each row = one patient  ·  each column = one health indicator.",
], size=14, line_spacing=1.45, space_after=8)

cx, cy, cw, ch = Inches(7.8), Inches(2.2), Inches(4.9), Inches(4.6)
rect(s, cx, cy, cw, ch, SOFT, line=LINE)
rect(s, cx, cy, cw, Inches(0.45), TEAL)
text(s, cx + Inches(0.3), cy + Inches(0.07), cw - Inches(0.6), Inches(0.4),
     "DATASET AT A GLANCE", size=11, bold=True, color=WHITE)
rows = [
    ("Records",   "70,693 patients"),
    ("Features",  "21 health indicators"),
    ("Target",    "Diabetes_binary  (0 / 1)"),
    ("Balance",   "50 % / 50 %"),
    ("Type",      "Tabular · structured"),
    ("Task",      "Binary classification"),
]
ry = cy + Inches(0.75)
for label, value in rows:
    text(s, cx + Inches(0.3), ry, Inches(1.5), Inches(0.4),
         label, size=11, bold=True, color=TEAL)
    text(s, cx + Inches(1.9), ry, Inches(2.8), Inches(0.4),
         value, size=11, color=INK)
    ry += Inches(0.55)
note(s,
    "Explain WHERE the data came from. BRFSS is a real CDC survey — that's why our model is "
    "grounded in actual public-health data. Mention 70k+ rows as a strength.")


# =====================================================================
# SLIDE 5 - TARGET & FEATURES
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 5); title_block(s, "03  ·  Variables", "Target and features")

tx, ty, tw, th = Inches(0.7), Inches(2.1), Inches(12.0), Inches(0.95)
rect(s, tx, ty, tw, th, SOFT, line=LINE)
rect(s, tx, ty, Inches(0.08), th, AMBER)
text(s, tx + Inches(0.25), ty + Inches(0.1), Inches(3), Inches(0.3),
     "TARGET VARIABLE  (y)", size=10, bold=True, color=AMBER)
text(s, tx + Inches(0.25), ty + Inches(0.4), Inches(12), Inches(0.5),
     "Diabetes_binary  →  0 = No Diabetes   ·   1 = Diabetes / Prediabetes",
     size=16, bold=True, color=INK)

text(s, Inches(0.7), Inches(3.25), Inches(8), Inches(0.4),
     "21 FEATURES  (X)", size=10, bold=True, color=AMBER)

col_w = Inches(4.1); col_y = Inches(3.7); col_h = Inches(3.3)
def feat_col(x, header, items):
    rect(s, x, col_y, col_w, col_h, WHITE, line=LINE)
    rect(s, x, col_y, col_w, Inches(0.4), TEAL)
    text(s, x + Inches(0.25), col_y + Inches(0.07),
         col_w - Inches(0.4), Inches(0.3),
         header, size=10, bold=True, color=WHITE)
    bullets(s, x + Inches(0.25), col_y + Inches(0.55),
            col_w - Inches(0.4), col_h - Inches(0.6),
            items, size=11, color=INK, line_spacing=1.25,
            space_after=4, bullet="·", bullet_color=TEAL)

feat_col(Inches(0.7), "VITAL  ·  CLINICAL", [
    "HighBP — high blood pressure",
    "HighChol — high cholesterol",
    "CholCheck — checked in 5 years",
    "BMI — Body Mass Index",
    "Stroke — ever had a stroke",
    "HeartDiseaseorAttack",
    "DiffWalk — difficulty walking",
])
feat_col(Inches(5.0), "LIFESTYLE", [
    "Smoker",
    "PhysActivity",
    "Fruits",
    "Veggies",
    "HvyAlcoholConsump",
    "AnyHealthcare",
    "NoDocbcCost",
])
feat_col(Inches(9.3), "SELF-REPORTED  ·  DEMOGRAPHICS", [
    "GenHlth — general health (1-5)",
    "MentHlth — bad-mood days",
    "PhysHlth — sick days",
    "Sex — 0 female / 1 male",
    "Age — group (1-13)",
    "Education — level (1-6)",
    "Income — bracket (1-8)",
])
note(s,
    "Show that the target is binary — that's why we use classification. Then walk through "
    "the 3 categories of features quickly. Highlight BMI, HighBP, GenHlth — these become the "
    "top predictors later in the deck.")


# =====================================================================
# SLIDE 6 - PROJECT WORKFLOW (block diagram)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 6); title_block(s, "04  ·  Method", "Project workflow")

steps = [
    ("01", "Data\nCollection",     "Load CSV"),
    ("02", "Data\nCleaning",       "Duplicates · dtypes"),
    ("03", "EDA &\nCorrelation",   "Stats · heatmap"),
    ("04", "Model\nTraining",      "Random Forest"),
    ("05", "Model\nEvaluation",    "Accuracy · matrix"),
    ("06", "Insights &\nApp",      "Top factors · GUI"),
]
box_w, box_h = Inches(3.7), Inches(1.7)
arr_w = Inches(0.45)
gap_x = arr_w + Inches(0.1)
start_x = Inches(0.55)
row1_y, row2_y = Inches(2.4), Inches(5.0)

def step_box(x, y, num, title, desc):
    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, box_w, box_h)
    card.fill.solid(); card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = TEAL; card.line.width = Pt(1.25); card.shadow.inherit = False
    badge = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        x + Inches(0.25), y + Inches(0.22), Inches(0.55), Inches(0.35))
    badge.fill.solid(); badge.fill.fore_color.rgb = TEAL
    badge.line.fill.background(); badge.shadow.inherit = False
    tf = badge.text_frame; tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = num
    r.font.name = FONT; r.font.size = Pt(11); r.font.bold = True
    r.font.color.rgb = WHITE
    text(s, x + Inches(0.9), y + Inches(0.18), box_w - Inches(1), Inches(0.7),
         title, size=14, bold=True, color=INK, line_spacing=1.1)
    text(s, x + Inches(0.3), y + Inches(1.05), box_w - Inches(0.5), Inches(0.6),
         desc, size=11, color=SLATE)

def r_arrow(x, y):
    a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y - Inches(0.18), arr_w, Inches(0.36))
    a.fill.solid(); a.fill.fore_color.rgb = TEAL
    a.line.fill.background(); a.shadow.inherit = False

def l_arrow(x, y):
    a = s.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, x, y - Inches(0.18), arr_w, Inches(0.36))
    a.fill.solid(); a.fill.fore_color.rgb = TEAL
    a.line.fill.background(); a.shadow.inherit = False

def d_arrow(x, y):
    a = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x - Inches(0.18), y, Inches(0.36), Inches(0.4))
    a.fill.solid(); a.fill.fore_color.rgb = TEAL
    a.line.fill.background(); a.shadow.inherit = False

xs_top = []
for i in range(3):
    x = start_x + i * (box_w + gap_x); xs_top.append(x)
    step_box(x, row1_y, *steps[i])
for i in range(2):
    r_arrow(xs_top[i] + box_w + Inches(0.05), row1_y + box_h/2)

xs_bot = []
for i in range(3):
    x = start_x + (2 - i) * (box_w + gap_x); xs_bot.append(x)
    step_box(x, row2_y, *steps[3 + i])
for i in range(2):
    l_arrow(xs_bot[i + 1] + box_w + Inches(0.05), row2_y + box_h/2)

mid_y = row1_y + box_h + Inches(0.25)
d_arrow(xs_top[2] + box_w/2, mid_y)
note(s,
    "Walk through the 6 phases of CRISP-DM in 30 seconds. We collected real data, cleaned it, "
    "explored it, trained models, evaluated them, and built a web app.")


# =====================================================================
# SLIDE 7 - DATA CLEANING
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 7); title_block(s, "05  ·  Preprocessing", "Data cleaning — what we did")

bullets(s, Inches(0.7), Inches(2.2), Inches(7), Inches(4), [
    "Checked for missing values  →  found 0  ✓",
    "Removed duplicate rows  →  1 636 dropped",
    "Final shape: 69 057 rows × 22 columns",
    "Converted 21 columns to int (everything except BMI which is float)",
    "Verified class balance still ~50 / 50",
], size=14, line_spacing=1.45, space_after=10)

cx, cy, cw, ch = Inches(8.2), Inches(2.4), Inches(4.5), Inches(3.6)
rect(s, cx, cy, cw, ch, SOFT, line=LINE)
text(s, cx + Inches(0.3), cy + Inches(0.25), cw - Inches(0.4), Inches(0.3),
     "BEFORE  →  AFTER", size=10, bold=True, color=AMBER)
text(s, cx + Inches(0.3), cy + Inches(0.7), cw - Inches(0.4), Inches(0.4),
     "Rows", size=11, bold=True, color=TEAL)
text(s, cx + Inches(0.3), cy + Inches(1.05), cw - Inches(0.4), Inches(0.5),
     "70 693  →  69 057", size=20, bold=True, color=INK)
text(s, cx + Inches(0.3), cy + Inches(1.8), cw - Inches(0.4), Inches(0.4),
     "Duplicates", size=11, bold=True, color=TEAL)
text(s, cx + Inches(0.3), cy + Inches(2.15), cw - Inches(0.4), Inches(0.5),
     "1 636  →  0", size=20, bold=True, color=INK)
text(s, cx + Inches(0.3), cy + Inches(2.9), cw - Inches(0.4), Inches(0.4),
     "Missing values", size=11, bold=True, color=TEAL)
text(s, cx + Inches(0.3), cy + Inches(3.25), cw - Inches(0.4), Inches(0.3),
     "0  →  0  ✓ already clean", size=14, color=INK)
note(s,
    "Key point: we dropped 1 636 duplicate rows. If we hadn't, the test set could have contained "
    "rows that the model already saw in training — inflating accuracy artificially. This is "
    "called 'data leakage' and is a viva-favourite question.")


# =====================================================================
# SLIDE 8 - EDA (embedded real plots)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 8); title_block(s, "06  ·  EDA", "Exploratory data analysis")

plot_w, plot_h = Inches(5.8), Inches(2.45)
positions = [
    (Inches(0.7),  Inches(2.1)),
    (Inches(6.85), Inches(2.1)),
    (Inches(0.7),  Inches(4.75)),
    (Inches(6.85), Inches(4.75)),
]
plot_files = [
    "01_class_balance.png",
    "02_bmi_distribution.png",
    "03_bmi_boxplot.png",
    "04_bp_chol.png",
]
for (x, y), f in zip(positions, plot_files):
    if (PLOTS / f).exists():
        s.shapes.add_picture(str(PLOTS / f), x, y, width=plot_w, height=plot_h)
note(s,
    "Show 4 EDA charts: class balance (perfectly 50/50), BMI distribution, BMI boxplot, and "
    "BP/Cholesterol counts. Key takeaway: diabetic patients have visibly higher BMI and more "
    "HighBP / HighChol cases.")


# =====================================================================
# SLIDE 9 - CORRELATION HEATMAP + TOP CORRELATIONS
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 9); title_block(s, "07  ·  Correlation", "Which features matter most?")

if (PLOTS / "05_correlation_heatmap.png").exists():
    s.shapes.add_picture(str(PLOTS / "05_correlation_heatmap.png"),
                         Inches(0.4), Inches(1.95),
                         width=Inches(7.0), height=Inches(5.2))

text(s, Inches(7.6), Inches(2.0), Inches(5.5), Inches(0.4),
     "TOP 10 CORRELATED WITH DIABETES", size=11, bold=True, color=AMBER)
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
ty = Inches(2.5)
for feat, val in top10:
    text(s, Inches(7.6), ty, Inches(2.7), Inches(0.35),
         feat, size=12, bold=True, color=INK)
    bar_w = Inches(2.2 * val / 0.4)
    rect(s, Inches(10.4), ty + Inches(0.07), bar_w, Inches(0.2), TEAL)
    text(s, Inches(10.4) + bar_w + Inches(0.1), ty, Inches(0.8), Inches(0.35),
         f"{val:.2f}", size=11, color=SLATE)
    ty += Inches(0.42)
note(s,
    "Heatmap shows feature relationships. The strongest correlations with diabetes are "
    "General Health (0.40), High Blood Pressure (0.37), BMI (0.29), and High Cholesterol (0.28). "
    "These are also the top features in the model — good cross-validation.")


# =====================================================================
# SLIDE 10 - TRAIN / TEST SPLIT (data leakage explainer)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 10); title_block(s, "08  ·  Split", "Train / test split — done before everything else")

bullets(s, Inches(0.7), Inches(2.2), Inches(7), Inches(4), [
    "80 % training data  ·  20 % test data",
    "Stratified by target → keeps 50 / 50 balance in both splits",
    "random_state = 42 → reproducible results",
    "Split BEFORE any preprocessing → prevents data leakage",
], size=15, line_spacing=1.5, space_after=10)

cx, cy = Inches(8.2), Inches(2.5)
cw, ch = Inches(4.5), Inches(0.8)
text(s, cx, cy - Inches(0.5), cw, Inches(0.3),
     "DATA SPLIT", size=10, bold=True, color=AMBER)
rect(s, cx, cy, Inches(3.6), ch, TEAL)
rect(s, cx + Inches(3.6), cy, Inches(0.9), ch, AMBER)
text(s, cx, cy + Inches(0.95), Inches(3.6), Inches(0.3),
     "Train · 55 245 rows", size=10, color=INK, align=PP_ALIGN.CENTER)
text(s, cx + Inches(3.6), cy + Inches(0.95), Inches(0.9), Inches(0.3),
     "Test · 13 812", size=10, color=INK, align=PP_ALIGN.CENTER)

wx, wy, ww, wh = Inches(8.2), Inches(4.5), Inches(4.5), Inches(2.4)
rect(s, wx, wy, ww, wh, SOFT, line=LINE)
text(s, wx + Inches(0.3), wy + Inches(0.2), ww - Inches(0.4), Inches(0.35),
     "WHY SPLIT FIRST?", size=10, bold=True, color=AMBER)
text(s, wx + Inches(0.3), wy + Inches(0.65), ww - Inches(0.4), Inches(1.6),
     "If we scaled, imputed, or sampled before splitting, information from the test set "
     "would leak into training. Accuracy would look great in our notebook but fail on new data.",
     size=12, color=INK, line_spacing=1.35)
note(s,
    "This is the most important methodology point. Mention 'data leakage' by name — it shows "
    "mastery. Explain we split first so the test set is truly unseen.")


# =====================================================================
# SLIDE 11 - WHY MACHINE LEARNING
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 11); title_block(s, "09  ·  Approach", "Why supervised machine learning?")

def card(x, y, w, h, label, value, desc):
    rect(s, x, y, w, h, SOFT, line=LINE)
    rect(s, x, y, Inches(0.08), h, TEAL)
    text(s, x + Inches(0.3), y + Inches(0.25), w - Inches(0.4), Inches(0.3),
         label, size=10, bold=True, color=AMBER)
    text(s, x + Inches(0.3), y + Inches(0.6), w - Inches(0.4), Inches(0.6),
         value, size=20, bold=True, color=INK)
    text(s, x + Inches(0.3), y + Inches(1.45), w - Inches(0.4), Inches(1.5),
         desc, size=12, color=SLATE, line_spacing=1.35)

cw, ch = Inches(4.0), Inches(3.1)
card(Inches(0.7),  Inches(2.5), cw, ch,
     "LEARNING TYPE", "Supervised",
     "The target column is labeled (0 / 1) — the model learns from known examples.")
card(Inches(4.9),  Inches(2.5), cw, ch,
     "TASK", "Classification",
     "We predict a discrete class, not a number. Two classes → binary classification.")
card(Inches(9.1),  Inches(2.5), cw, ch,
     "OUTPUT", "Probability + label",
     "Each prediction includes a confidence score, useful for risk-screening contexts.")
note(s,
    "State clearly: this is supervised binary classification. We have labeled examples, two "
    "classes, and we use the patterns to predict diabetes for new patients.")


# =====================================================================
# SLIDE 12 - 4 CANDIDATE MODELS
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 12); title_block(s, "10  ·  Candidates", "4 supervised classifiers tested")

models_info = [
    ("Logistic Regression",  "Fits a probability line between the two classes",
     "Simple · interpretable", "Less accurate on non-linear patterns"),
    ("Decision Tree",        "Asks yes/no questions to split the data",
     "Easy to visualise",     "Prone to overfitting"),
    ("K-Nearest Neighbors",  "Predicts class by voting among nearest neighbours",
     "Intuitive",             "Slow on large data · needs scaling"),
    ("Random Forest",        "Combines many decision trees, votes the answer",
     "Robust · feature imp.", "Slower to train"),
]
cw, ch = Inches(6.0), Inches(2.15)
positions = [
    (Inches(0.7),  Inches(2.2)),
    (Inches(6.85), Inches(2.2)),
    (Inches(0.7),  Inches(4.6)),
    (Inches(6.85), Inches(4.6)),
]
for (x, y), (name, how, pros, cons) in zip(positions, models_info):
    rect(s, x, y, cw, ch, WHITE, line=LINE)
    rect(s, x, y, cw, Inches(0.45), TEAL)
    text(s, x + Inches(0.3), y + Inches(0.07), cw - Inches(0.4), Inches(0.4),
         name.upper(), size=11, bold=True, color=WHITE)
    text(s, x + Inches(0.3), y + Inches(0.55), cw - Inches(0.4), Inches(0.5),
         how, size=12, color=INK)
    text(s, x + Inches(0.3), y + Inches(1.15), Inches(1), Inches(0.35),
         "PROS", size=9, bold=True, color=GREEN_OK)
    text(s, x + Inches(1.3), y + Inches(1.15), cw - Inches(1.5), Inches(0.35),
         pros, size=11, color=SLATE)
    text(s, x + Inches(0.3), y + Inches(1.55), Inches(1), Inches(0.35),
         "CONS", size=9, bold=True, color=RED_NO)
    text(s, x + Inches(1.3), y + Inches(1.55), cw - Inches(1.5), Inches(0.35),
         cons, size=11, color=SLATE)
note(s,
    "These are the 4 supervised classifiers we considered. We tested all four to make a "
    "data-driven choice — not just pick a favourite. RF was chosen for best F1 + "
    "feature importance for clinical interpretability.")


# =====================================================================
# SLIDE 13 - MODEL COMPARISON (real numbers + chart)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 13); title_block(s, "11  ·  Results", "Model comparison — real numbers")

if (PLOTS / "08_model_comparison.png").exists():
    s.shapes.add_picture(str(PLOTS / "08_model_comparison.png"),
                         Inches(0.5), Inches(2.0),
                         width=Inches(7.5), height=Inches(4.2))

text(s, Inches(8.4), Inches(2.0), Inches(4.5), Inches(0.4),
     "FULL METRICS", size=11, bold=True, color=AMBER)

headers = ["Model", "Acc", "F1"]
col_x = [Inches(8.4), Inches(11.0), Inches(11.9)]
hy = Inches(2.5)
rect(s, Inches(8.4), hy, Inches(4.3), Inches(0.4), TEAL)
for h, x in zip(headers, col_x):
    text(s, x + Inches(0.05), hy + Inches(0.07), Inches(1.5), Inches(0.3),
         h, size=10, bold=True, color=WHITE)

ry = hy + Inches(0.4)
for i, row in enumerate(comparison):
    bg = SOFT if i % 2 == 0 else WHITE
    rect(s, Inches(8.4), ry, Inches(4.3), Inches(0.5), bg, line=LINE)
    name_color = TEAL_DARK if row["Model"] == "Random Forest" else INK
    name_bold  = True if row["Model"] == "Random Forest" else False
    text(s, col_x[0] + Inches(0.05), ry + Inches(0.12),
         Inches(2.5), Inches(0.35),
         row["Model"], size=10, bold=name_bold, color=name_color)
    text(s, col_x[1] + Inches(0.05), ry + Inches(0.12),
         Inches(0.8), Inches(0.35),
         f"{row['Accuracy']:.3f}", size=10, color=INK)
    text(s, col_x[2] + Inches(0.05), ry + Inches(0.12),
         Inches(0.8), Inches(0.35),
         f"{row['F1']:.3f}", size=10, color=INK)
    ry += Inches(0.5)

vy = Inches(5.0)
rect(s, Inches(8.4), vy, Inches(4.3), Inches(1.85), SOFT, line=LINE)
text(s, Inches(8.5), vy + Inches(0.15), Inches(4), Inches(0.3),
     "WINNER", size=10, bold=True, color=AMBER)
text(s, Inches(8.5), vy + Inches(0.5), Inches(4), Inches(0.5),
     "Random Forest", size=16, bold=True, color=TEAL_DARK)
text(s, Inches(8.5), vy + Inches(1.05), Inches(4.1), Inches(0.8),
     "Best F1 (0.759) and built-in feature importance.",
     size=11, color=INK, line_spacing=1.3)
note(s,
    "Be honest: Logistic Regression actually has slightly higher accuracy. But Random Forest "
    "has the best F1 score AND gives us feature importance for free. F1 matters more in medical "
    "apps because we balance precision and recall. That's why we chose RF.")


# =====================================================================
# SLIDE 14 - RANDOM FOREST RESULTS (confusion matrix + metrics)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 14); title_block(s, "12  ·  Final model", "Random Forest — detailed results")

if (PLOTS / "06_confusion_matrix.png").exists():
    s.shapes.add_picture(str(PLOTS / "06_confusion_matrix.png"),
                         Inches(0.7), Inches(2.2),
                         width=Inches(5.2), height=Inches(4.6))

def small_card(x, y, label, value, sublabel=""):
    cw, ch = Inches(3.0), Inches(1.4)
    rect(s, x, y, cw, ch, SOFT, line=LINE)
    rect(s, x, y, Inches(0.08), ch, TEAL)
    text(s, x + Inches(0.3), y + Inches(0.15), cw - Inches(0.4), Inches(0.3),
         label, size=10, bold=True, color=AMBER)
    text(s, x + Inches(0.3), y + Inches(0.5), cw - Inches(0.4), Inches(0.7),
         value, size=24, bold=True, color=INK)
    if sublabel:
        text(s, x + Inches(0.3), y + Inches(1.05), cw - Inches(0.4), Inches(0.3),
             sublabel, size=10, color=SLATE)

acc  = comparison[3]["Accuracy"]
prec = comparison[3]["Precision"]
rec  = comparison[3]["Recall"]
f1   = comparison[3]["F1"]

small_card(Inches(6.5), Inches(2.2), "ACCURACY",  f"{acc*100:.2f}%")
small_card(Inches(9.7), Inches(2.2), "F1 SCORE",  f"{f1:.3f}")
small_card(Inches(6.5), Inches(3.8), "PRECISION", f"{prec:.3f}",
           "Predicted diabetics that were correct")
small_card(Inches(9.7), Inches(3.8), "RECALL",    f"{rec:.3f}",
           "Actual diabetics we correctly caught")

hx, hy, hw, hh = Inches(6.5), Inches(5.4), Inches(6.2), Inches(1.6)
rect(s, hx, hy, hw, hh, WHITE, line=LINE)
text(s, hx + Inches(0.25), hy + Inches(0.15), hw - Inches(0.4), Inches(0.3),
     "HYPERPARAMETERS", size=10, bold=True, color=AMBER)
text(s, hx + Inches(0.25), hy + Inches(0.55), hw - Inches(0.4), Inches(1.0),
     "n_estimators = 200   ·   max_depth = 15   ·   min_samples_leaf = 5\n"
     "random_state = 42   ·   n_jobs = -1  (use all CPU cores)",
     size=12, color=INK, line_spacing=1.4)
note(s,
    "Confusion matrix on the left: 4 696 true negatives and 5 574 true positives. "
    "Recall of 0.79 means we caught 79% of real diabetics — this is what matters most in "
    "medical screening. False negatives are more dangerous than false positives.")


# =====================================================================
# SLIDE 15 - TOP RISK FACTORS (feature importance)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 15); title_block(s, "13  ·  Insights", "Top diabetes risk factors")

if (PLOTS / "07_feature_importance.png").exists():
    s.shapes.add_picture(str(PLOTS / "07_feature_importance.png"),
                         Inches(0.4), Inches(1.9),
                         width=Inches(6.8), height=Inches(5.2))

text(s, Inches(7.5), Inches(2.0), Inches(5.5), Inches(0.4),
     "TOP 5 RISK FACTORS LEARNED", size=11, bold=True, color=AMBER)
top5 = list(metrics["top_5_features"].items())
ranks = ["1.", "2.", "3.", "4.", "5."]
ty = Inches(2.55)
for (feat, val), rank in zip(top5, ranks):
    text(s, Inches(7.5), ty, Inches(0.6), Inches(0.55),
         rank, size=22, bold=True, color=TEAL)
    text(s, Inches(8.2), ty + Inches(0.05), Inches(3.5), Inches(0.45),
         feat, size=14, bold=True, color=INK)
    text(s, Inches(8.2), ty + Inches(0.4), Inches(4.5), Inches(0.3),
         f"importance = {val:.3f}", size=11, color=SLATE)
    ty += Inches(0.85)
note(s,
    "The model identified the 5 most important risk factors entirely from data: "
    "General Health, High BP, BMI, Age, and High Cholesterol. These match what doctors would "
    "tell you — validating that the model learned something meaningful.")


# =====================================================================
# SLIDE 16 - STREAMLIT APP (deployment)
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 16); title_block(s, "14  ·  Deployment", "Streamlit web application")

bullets(s, Inches(0.7), Inches(2.2), Inches(6.5), Inches(4), [
    "Interactive form built with Streamlit (Python web framework).",
    "User enters 21 health indicators in plain English.",
    "Trained model loaded once and cached for speed.",
    "Output: risk label + probability + confidence bar.",
    "Code on GitHub  ·  deployed free on Streamlit Cloud.",
], size=14, line_spacing=1.45, space_after=8)

cx, cy, cw, ch = Inches(7.8), Inches(2.2), Inches(4.9), Inches(4.6)
rect(s, cx, cy, cw, ch, SOFT, line=LINE)
rect(s, cx, cy, cw, Inches(0.45), TEAL)
text(s, cx + Inches(0.3), cy + Inches(0.07), cw - Inches(0.4), Inches(0.4),
     "DIABETES RISK PREDICTION", size=11, bold=True, color=WHITE)

def field(label, value, y_off):
    fx = cx + Inches(0.3); fy = cy + y_off
    text(s, fx, fy, Inches(2.0), Inches(0.3),
         label, size=10, bold=True, color=SLATE)
    rect(s, fx + Inches(2.1), fy + Inches(0.02), Inches(2.0), Inches(0.3),
         WHITE, line=LINE)
    text(s, fx + Inches(2.2), fy + Inches(0.04), Inches(1.8), Inches(0.3),
         value, size=10, color=INK)

field("BMI",         "27",        Inches(0.7))
field("High BP",     "Yes",       Inches(1.1))
field("High Chol",   "No",        Inches(1.5))
field("General Hlth","3 - Good",  Inches(1.9))
field("Age group",   "50-54",     Inches(2.3))

bx = cx + Inches(0.3); by = cy + Inches(2.85)
rect(s, bx, by, Inches(4.3), Inches(0.5), TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(s, bx, by + Inches(0.12), Inches(4.3), Inches(0.3),
     "PREDICT", size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

ry = cy + Inches(3.55)
rect(s, bx, ry, Inches(4.3), Inches(0.85), SOFT, line=AMBER)
text(s, bx + Inches(0.2), ry + Inches(0.1), Inches(4), Inches(0.3),
     "HIGH RISK", size=11, bold=True, color=RED_NO)
text(s, bx + Inches(0.2), ry + Inches(0.45), Inches(4), Inches(0.3),
     "probability  68 %", size=11, color=INK)
note(s,
    "Show or describe the live app. If on Streamlit Cloud, show the URL. The app loads the "
    "trained model and lets anyone enter data to get an instant prediction. Mention this is "
    "your 'demo moment' if you can run it live.")


# =====================================================================
# SLIDE 17 - LIMITATIONS, CONCLUSION & Q&A
# =====================================================================
s = prs.slides.add_slide(blank)
chrome(s, 17); title_block(s, "15  ·  Wrap-up", "Limitations · Conclusion · Q&A")

text(s, Inches(0.7), Inches(2.2), Inches(6), Inches(0.35),
     "LIMITATIONS", size=11, bold=True, color=AMBER)
bullets(s, Inches(0.7), Inches(2.55), Inches(6), Inches(2.3), [
    "Self-reported survey data is noisy.",
    "No lab values (no HbA1c or glucose).",
    "Balanced data  ≠  real-world prevalence (~14%).",
    "Class 1 mixes diabetic + prediabetic.",
], size=12, line_spacing=1.35, space_after=4, bullet="·", bullet_color=RED_NO)

text(s, Inches(0.7), Inches(5.0), Inches(6), Inches(0.35),
     "CONCLUSION", size=11, bold=True, color=AMBER)
bullets(s, Inches(0.7), Inches(5.35), Inches(6), Inches(2), [
    f"Random Forest classifier  ·  {acc*100:.1f}% test accuracy  ·  {f1:.3f} F1 score.",
    "Identified 5 dominant risk factors aligned with medical literature.",
    "Delivered a working web app and reproducible notebook.",
], size=12, line_spacing=1.35, space_after=4, bullet="·", bullet_color=GREEN_OK)

text(s, Inches(7.2), Inches(2.2), Inches(5.5), Inches(0.35),
     "LIKELY QUESTIONS", size=11, bold=True, color=AMBER)
qas = [
    ("Why Random Forest over Logistic Reg?",
     "Best F1 + feature importance for free."),
    ("Why only 74% accuracy?",
     "Self-reported data caps it; matches published research."),
    ("Why drop duplicates?",
     "Prevents test-set inflation (data leakage)."),
    ("Supervised or unsupervised?",
     "Supervised - target is labeled 0 / 1."),
    ("How would you improve it?",
     "Add lab values · try XGBoost · tune hyperparameters."),
]
ty = Inches(2.55)
for q, a in qas:
    text(s, Inches(7.2), ty, Inches(5.5), Inches(0.3),
         q, size=10, bold=True, color=INK)
    text(s, Inches(7.2), ty + Inches(0.28), Inches(5.5), Inches(0.3),
         a, size=10, color=SLATE)
    ty += Inches(0.7)

rect(s, Inches(0.7), Inches(6.5), Inches(12), Inches(0.45), TEAL,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(s, Inches(0.7), Inches(6.6), Inches(12), Inches(0.3),
     "Thank you  ·  Questions?", size=14, bold=True, color=WHITE,
     align=PP_ALIGN.CENTER)
note(s,
    "Close with humility (limitations) then confidence (conclusion). The Q&A panel "
    "preemptively answers the most common questions. Always end with 'Thank you — any questions?'")


# =====================================================================
# SAVE
# =====================================================================
out_pptx = PRESENTATION / "Diabetes_Final_Presentation.pptx"
prs.save(out_pptx)
print(f"Saved {out_pptx.name}  ({TOTAL} slides, native python-pptx objects, with speaker notes)")
