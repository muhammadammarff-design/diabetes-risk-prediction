# 📤 GitHub Setup Guide — Drag-and-Drop Upload

This guide shows you how to push the project to GitHub **without using the command line**.
Just create an empty repo on GitHub and drag-and-drop the entire folder into it.

> ⏱️ Takes about 3 minutes.

---

## Step 1 — Create a new empty GitHub repository

1. Open https://github.com/new in your browser
2. Fill in:
   - **Repository name**: `Diabetes-Risk-Prediction`
   - **Description**: `Diabetes Risk Prediction using Machine Learning and BRFSS Health Indicators (IDS Semester Project)`
   - **Public** (so the instructor can see it)
   - ❌ Do **NOT** tick "Add a README file" (we have our own)
   - ❌ Do **NOT** add .gitignore (we have our own)
3. Click **Create repository**
4. You'll see a page with upload instructions — keep it open.

---

## Step 2 — Prepare the folder

1. Open the `Diabetes_Project/` folder on your computer.
2. Make sure these files and folders are inside it (this is everything we are uploading):

```
Diabetes_Project/                  ← upload THIS entire folder
│
├── app/
│   └── streamlit_app.py
├── data/
│   └── diabetes_binary_5050split_health_indicators_BRFSS2015.csv
├── docs/
│   ├── PROJECT_ROADMAP.md
│   ├── SETUP_GUIDE.md
│   ├── Speaker_Notes.md          ← important for viva!
│   └── GITHUB_SETUP.md           ← this file
├── models/
│   ├── rf_model.joblib           ← 74 MB
│   ├── feature_names.json
│   ├── metrics.json
│   ├── model_comparison.csv
│   └── model_comparison.json
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
│   ├── 08_model_comparison.png
│   └── 09_streamlit_app.png
├── presentation/
│   ├── Diabetes_Final_Presentation.pptx
│   ├── Diabetes_Final_Presentation.pdf
│   ├── Diabetes_Project_Proposal.pptx
│   └── Diabetes_Project_Proposal.pdf
├── scripts/
│   ├── train_model.py
│   ├── compare_models.py
│   ├── enhance_plots.py
│   └── build_ppt.py
├── .gitignore
├── .streamlit/
│   └── config.toml
├── README.md
├── requirements.txt
└── runtime.txt
```

3. **Do NOT include** (these should NOT be uploaded):
   * `venv/` (virtual environment)
   * `__pycache__/` folders
   * `.DS_Store` files
   * `*.tmp` files

   These are blocked automatically by `.gitignore`, so don't worry if they exist.

---

## Step 3 — Drag and drop

On the empty GitHub repo page:

1. Scroll down to the section titled **"…or create a new file on the start screen"**
2. You will see a big box that says **"Drag files here to add them to your repository"**
3. Open your file manager (Explorer / Finder) in another window
4. Select everything **inside** `Diabetes_Project/` (NOT the folder itself):
   * All subfolders: `app/`, `data/`, `docs/`, `models/`, `notebooks/`, `plots/`, `presentation/`, `scripts/`, `.streamlit/`
   * All loose files: `.gitignore`, `README.md`, `requirements.txt`, `runtime.txt`
5. Drag the selection into the upload box on GitHub.
6. Wait for the upload (could take 1–2 minutes because of the dataset + model).

> 💡 **Tip**: If GitHub refuses to upload everything at once, do it in 2 batches:
> * First batch: folders `data/`, `models/`, `plots/`, `presentation/`
> * Second batch: everything else

---

## Step 4 — Commit

After all files finish uploading:

1. Scroll to the bottom of the upload box.
2. Add a commit message: `Initial commit — Diabetes Risk Prediction project`
3. Click **Commit changes**.

Your repo is now live 🎉

---

## Step 5 — Verify

Open your repo and check:

* ✅ `README.md` is the default landing page
* ✅ `presentation/Diabetes_Final_Presentation.pptx` is downloadable
* ✅ `docs/Speaker_Notes.md` is readable on GitHub
* ✅ `data/` shows the CSV file
* ✅ `models/rf_model.joblib` is uploaded (74 MB is OK on free GitHub)

If anything is missing, you can click **Add file → Upload files** again and add it.

---

## (Optional) Step 6 — Deploy Streamlit

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Pick your `Diabetes-Risk-Prediction` repo
5. Set **Main file path** = `app/streamlit_app.py`
6. Click **Deploy**
7. After ~1 minute you'll get a public URL like:
   `https://your-name-diabetes-risk.streamlit.app`
8. Test it: enter values, click **Predict**
9. Save that URL for your viva demo.

---

## Quick recap

| What to upload | Where |
|---|---|
| Source code (`scripts/`, `app/`, `notebooks/`) | drag-and-drop |
| Data (`data/`) | drag-and-drop |
| Plots (`plots/`) | drag-and-drop |
| Presentation (`presentation/`) | drag-and-drop |
| Trained model (`models/`) | drag-and-drop |
| Docs (`docs/`, `README.md`) | drag-and-drop |
| Config files (`.gitignore`, `requirements.txt`) | drag-and-drop |
| venv / caches / __pycache__ | **DO NOT upload** |

---

## If something goes wrong

### "File larger than 25 MB"
The `models/rf_model.joblib` is saved with `joblib.dump(..., compress=3)` and is ~18 MB — well under GitHub's 25 MB web-upload limit. **All files in this project are under 25 MB**, so drag-and-drop will work without Git LFS.

If you ever retrain the model and it grows back above 25 MB, run this one-liner to shrink it:
```bash
python -c "import joblib; m = joblib.load('models/rf_model.joblib'); joblib.dump(m, 'models/rf_model.joblib', compress=3)"
```

### "YAML lint error in workflow file"
You didn't add one — ignore.

### "Upload got stuck"
Refresh the page and try again. GitHub will remember what was uploaded.

### "I forgot to include a file"
Just go to the folder on GitHub, click **Add file → Upload files**, and upload the missing one.

---

## ✅ Final check before viva

Once everything is on GitHub, confirm:

- [x] Repo is **Public**
- [x] README displays nicely on the repo homepage
- [x] PPT file is downloadable
- [x] Streamlit Cloud URL works in a browser
- [x] Speaker notes are printed for the team
- [x] All 3 team members are added as collaborators (Settings → Collaborators)

Good luck! 🎓
