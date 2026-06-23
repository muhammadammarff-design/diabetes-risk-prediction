# Diabetes Risk Prediction — Speaker Notes

**Team:** Ali Raza (2540010) · M. Ammar (2540004) · Taha Ali (2540008)  
**Instructor:** Sir Zaki  
**Course:** Introduction to Data Science, Semester 2  
**Project:** Diabetes Risk Prediction using Machine Learning

---

These notes are **embedded inside** `presentation/Diabetes_Final_Presentation.pptx` (open in PowerPoint → View → Notes Page). This file is a printable copy for viva preparation.

---

## Slide 1 — Title

Greet the audience. State project title, team and instructor. Keep brief — 30 seconds. Move to the next slide.

## Slide 2 — Outline

Walk through the outline in 30 seconds. We added an 'Our Model' slide early so the audience knows from the start which algorithm we used. The flow is: Problem → Data → Model → Method → Results → Demo → Conclusion.

## Slide 3 — The diabetes problem

Open with the human impact. 'Diabetes is not a small problem — 537 million adults have it.' This frames why our project matters. Don't dwell more than 1 minute.

## Slide 4 — Dataset overview

Explain WHERE the data came from. BRFSS is a real CDC survey — that's why our model is grounded in actual public-health data. Emphasize the **21 features** count — this is what sir expects to hear explicitly.

## Slide 5 — Target and selected features

Mention the 21 features are split into 3 categories. Highlight the SELECTED features shown in amber — these are the 5 most important ones according to our Random Forest model. Highlighted items in each column are the selected ones.

## Slide 6 — Our model (Random Forest)

Introduce the model upfront so the audience knows what we'll be training. ONE sentence explanation: 'A team of 200 decision trees that vote on the answer.' Then show the simple diagram. Why this model: best F1 + feature importance. Keep it under 1 minute.

## Slide 7 — Block diagram: Input → Methodology → Output

This is THE block diagram sir wants. Three layers stacked vertically: INPUT on top (the raw data), METHODOLOGY in the middle (the 4 steps we performed), OUTPUT at the bottom (the actual numbers we got). Walk through them in 30 seconds — top to bottom.

## Slide 8 — Data cleaning

Key point: we dropped 1 636 duplicate rows. If we hadn't, the test set could have contained rows that the model already saw in training — inflating accuracy artificially. This is called 'data leakage' and is a viva-favourite question.

## Slide 9 — Exploratory data analysis

Show 4 EDA charts: class balance (perfectly 50/50), BMI distribution, BMI boxplot, and BP/Cholesterol counts. Key takeaway: diabetic patients have visibly higher BMI and more HighBP / HighChol cases.

## Slide 10 — Which features matter most?

Heatmap shows feature relationships. The strongest correlations with diabetes are General Health (0.40), High Blood Pressure (0.37), BMI (0.29), and High Cholesterol (0.28). These are also the top features in the model — good cross-validation.

## Slide 11 — Train / test split

This is the most important methodology point. Mention 'data leakage' by name — it shows mastery. Explain we split first so the test set is truly unseen.

## Slide 12 — Why supervised machine learning?

State clearly: this is supervised binary classification. We have labeled examples, two classes, and we use the patterns to predict diabetes for new patients.

## Slide 13 — 4 supervised classifiers tested

These are the 4 supervised classifiers we considered. Random Forest (bottom-right) is highlighted with an amber border because we selected it. We tested all four to make a data-driven choice — not just pick a favourite.

## Slide 14 — Model comparison

Be honest: Logistic Regression actually has slightly higher accuracy. But Random Forest has the best F1 score AND gives us feature importance for free. F1 matters more in medical apps because we balance precision and recall. That's why we chose RF.

## Slide 15 — Random Forest — detailed results

Confusion matrix on the left: 4 696 true negatives and 5 574 true positives. Recall of 0.79 means we caught 79% of real diabetics — this is what matters most in medical screening. False negatives are more dangerous than false positives. The 4 metric cards on the right are deliberately LARGE — sir values clear, prominent results.

## Slide 16 — Top diabetes risk factors

The model identified the 5 most important risk factors entirely from data: General Health, High BP, BMI, Age, and High Cholesterol. These match what doctors would tell you — validating that the model learned something meaningful.

## Slide 17 — Streamlit web application

Show or describe the live app. If on Streamlit Cloud, show the URL. The app loads the trained model and lets anyone enter data to get an instant prediction. Mention this is your 'demo moment' if you can run it live.

## Slide 18 — Conclusion & results

This is THE conclusion slide — 4 BIG metric badges at the top show results PROMINENTLY (this is what gets marks for 'how we show results'). Below them: conclusion bullets (left), limitations (left), and likely Q&A (right). End with 'Thank you — any questions?'.
