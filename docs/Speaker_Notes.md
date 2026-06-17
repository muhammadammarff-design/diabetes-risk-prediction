# Diabetes Risk Prediction — Speaker Notes

**Team:** Ali Raza (2540010) · Muhammad Ammar (2540008) · Taha Ali (2540008)  
**Instructor:** Sir Zaki  
**Course:** Introduction to Data Science, Semester 2  
**Project:** Diabetes Risk Prediction using Machine Learning

---

These notes are **embedded inside** `presentation/Diabetes_Final_Presentation.pptx` (open in PowerPoint → View → Notes Page). This file is a printable copy for viva preparation and team rehearsals.

---

## Slide 1 — Title

Greet the audience. State project title, team and instructor. Keep brief — 30 seconds. Move to the next slide.

## Slide 2 — Outline

Walk through the outline in 30 seconds. Tell the audience the talk is structured as Problem → Data → Method → Results → Demo → Conclusion.

## Slide 3 — The diabetes problem

Open with the human impact. 'Diabetes is not a small problem — 537 million adults have it.' This frames why our project matters. Don't dwell more than 1 minute.

## Slide 4 — Dataset overview

Explain WHERE the data came from. BRFSS is a real CDC survey — that's why our model is grounded in actual public-health data. Mention 70k+ rows as a strength.

## Slide 5 — Target and features

Show that the target is binary — that's why we use classification. Then walk through the 3 categories of features quickly. Highlight BMI, HighBP, GenHlth — these become the top predictors later in the deck.

## Slide 6 — Project workflow

Walk through the 6 phases of CRISP-DM in 30 seconds. We collected real data, cleaned it, explored it, trained models, evaluated them, and built a web app.

## Slide 7 — Data cleaning

Key point: we dropped 1 636 duplicate rows. If we hadn't, the test set could have contained rows that the model already saw in training — inflating accuracy artificially. This is called 'data leakage' and is a viva-favourite question.

## Slide 8 — Exploratory data analysis

Show 4 EDA charts: class balance (perfectly 50/50), BMI distribution, BMI boxplot, and BP/Cholesterol counts. Key takeaway: diabetic patients have visibly higher BMI and more HighBP / HighChol cases.

## Slide 9 — Which features matter most?

Heatmap shows feature relationships. The strongest correlations with diabetes are General Health (0.40), High Blood Pressure (0.37), BMI (0.29), and High Cholesterol (0.28). These are also the top features in the model — good cross-validation.

## Slide 10 — Train / test split

This is the most important methodology point. Mention 'data leakage' by name — it shows mastery. Explain we split first so the test set is truly unseen.

## Slide 11 — Why supervised machine learning?

State clearly: this is supervised binary classification. We have labeled examples, two classes, and we use the patterns to predict diabetes for new patients.

## Slide 12 — 4 supervised classifiers tested

These are the 4 supervised classifiers we considered. We tested all four to make a data-driven choice — not just pick a favourite. RF was chosen for best F1 + feature importance for clinical interpretability.

## Slide 13 — Model comparison

Be honest: Logistic Regression actually has slightly higher accuracy. But Random Forest has the best F1 score AND gives us feature importance for free. F1 matters more in medical apps because we balance precision and recall. That's why we chose RF.

## Slide 14 — Random Forest — detailed results

Confusion matrix on the left: 4 696 true negatives and 5 574 true positives. Recall of 0.79 means we caught 79% of real diabetics — this is what matters most in medical screening. False negatives are more dangerous than false positives.

## Slide 15 — Top diabetes risk factors

The model identified the 5 most important risk factors entirely from data: General Health, High BP, BMI, Age, and High Cholesterol. These match what doctors would tell you — validating that the model learned something meaningful.

## Slide 16 — Streamlit web application

Show or describe the live app. If on Streamlit Cloud, show the URL. The app loads the trained model and lets anyone enter data to get an instant prediction. Mention this is your 'demo moment' if you can run it live.

## Slide 17 — Limitations · Conclusion · Q&A

Close with humility (limitations) then confidence (conclusion). The Q&A panel preemptively answers the most common questions. Always end with 'Thank you — any questions?'
