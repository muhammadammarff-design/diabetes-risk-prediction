# 🚀 Complete Setup Guide

This guide walks you through running the project locally **and** deploying it online — step by step. No prior experience needed.

---

## PART 1 · Run Locally in VSCode

### 1.1 Install prerequisites (one-time)

| Tool | Where to get it |
|---|---|
| **Python 3.11** | <https://www.python.org/downloads/> · ✅ tick *"Add Python to PATH"* during install |
| **VS Code**     | <https://code.visualstudio.com> |
| **VS Code Python extension** | Search "Python" in the Extensions tab and install (Microsoft) |
| **Git**         | <https://git-scm.com/downloads> |

Verify Python is installed:
```bash
python --version          # should print Python 3.11.x
```

### 1.2 Open the project in VSCode

1. Download / unzip the `diabetes_project` folder
2. In VSCode: **File → Open Folder → select `diabetes_project`**
3. Open the integrated terminal: **View → Terminal** (or `Ctrl + ~`)

### 1.3 Create an isolated environment

```bash
# create a virtual environment named 'venv'
python -m venv venv

# activate it
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (cmd):
venv\Scripts\activate.bat
# Mac / Linux:
source venv/bin/activate
```
You'll see `(venv)` appear at the start of your prompt — that confirms it worked.

### 1.4 Install the dependencies

```bash
pip install -r requirements.txt
```
Takes 1–2 minutes. Installs pandas, numpy, scikit-learn, matplotlib, seaborn, joblib, streamlit.

### 1.5 Train the model

```bash
python scripts/train_model.py
```
Watch the terminal — you'll see all 10 steps run. Takes ~30 seconds. Creates:
- `models/rf_model.joblib` — the trained Random Forest
- `models/feature_names.json` — column order
- `models/metrics.json` — accuracy & top features
- `plots/01_*.png` to `plots/07_*.png` — all charts

### 1.6 Launch the Streamlit web app

```bash
streamlit run app/streamlit_app.py
```
The terminal prints a URL like `http://localhost:8501` and your browser opens automatically.
Fill the form, click **Predict Diabetes Risk**, see the result.

To stop the app: press `Ctrl + C` in the terminal.

### 1.7 (Optional) Run the Jupyter notebook

In VSCode, just **open `notebooks/diabetes_analysis.ipynb`** — VSCode will detect the kernel and you can run cells with `Shift + Enter`.

---

## PART 2 · Push the Project to GitHub

GitHub stores your code online so you can share it, deploy it, and show it in your portfolio.

### 2.1 Create a GitHub account
Sign up at <https://github.com> (free).

### 2.2 Create a new repository (online)

1. Click the **+** icon (top-right) → **New repository**
2. Repository name: `diabetes-risk-prediction`
3. Description: *"Diabetes risk prediction using Random Forest and Streamlit"*
4. Set as **Public** (required for free Streamlit Cloud deployment)
5. **Don't** tick "Add a README" — we already have one
6. Click **Create repository**

GitHub will show you setup commands — keep that page open.

### 2.3 Push your local code (one-time)

In the VSCode terminal, inside the `diabetes_project` folder:

```bash
# 2.3a — initialise git in the project folder
git init
git branch -M main

# 2.3b — tell git who you are (only needed once on your computer)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 2.3c — stage and commit all the files
git add .
git commit -m "Initial commit: complete diabetes prediction project"

# 2.3d — connect to your GitHub repo (copy the URL from GitHub's setup page)
git remote add origin https://github.com/<your-username>/diabetes-risk-prediction.git

# 2.3e — push to GitHub
git push -u origin main
```

GitHub will ask for credentials. Use a **Personal Access Token** instead of your password:
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)
- Scopes: tick **repo**
- Copy the token and paste it as the password when prompted.

### 2.4 Verify

Refresh your GitHub repo page — you should see all your files there. ✅

### 2.5 Daily workflow (after the first push)

```bash
git add .
git commit -m "Short description of what changed"
git push
```

---

## PART 3 · Deploy to Streamlit Cloud (FREE)

Get a public URL anyone can visit — like `https://your-name-diabetes.streamlit.app`.

### 3.1 Sign up

1. Go to <https://streamlit.io/cloud>
2. Click **Sign up** → continue with GitHub
3. Authorise Streamlit to access your repositories

### 3.2 Deploy

1. From your Streamlit Cloud dashboard, click **New app**
2. Fill in:
   - **Repository:** `<your-username>/diabetes-risk-prediction`
   - **Branch:** `main`
   - **Main file path:** `app/streamlit_app.py`
   - **App URL:** choose a name (e.g. `diabetes-risk-2540010`)
3. Click **Deploy**

Streamlit Cloud will:
- Install dependencies from `requirements.txt` ✅
- Use Python 3.11 from `runtime.txt` ✅
- Build & start the app (takes 3–5 minutes the first time)

### 3.3 Verify

Once you see *"Your app is live!"*, click **Open**. Test the form — it should work exactly like local.

### 3.4 Re-deploy on changes

Every time you `git push`, Streamlit Cloud auto-rebuilds and re-deploys. No manual step needed. 🎉

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Reinstall Python and tick "Add to PATH" |
| `pip install` very slow | Use a different network, or run with `pip install -r requirements.txt --timeout 100` |
| `streamlit: command not found` | Activate the venv first (step 1.3) |
| Streamlit Cloud build fails: "model not found" | The `models/` folder must be committed. Check `.gitignore` doesn't exclude it. |
| Streamlit Cloud build fails: "module not found" | Add the missing package to `requirements.txt` and push again. |
| Git asks for password every push | Use SSH instead of HTTPS, or store the PAT in Git Credential Manager. |
| Browser shows "This site can't be reached" | Streamlit's URL is shown in the terminal — check you copied it fully. |

---

## ✅ You're done

You now have:
- A trained machine-learning model
- A working web app on your laptop
- The same app deployed online with a public URL
- Everything backed up on GitHub

Share the Streamlit URL in your final viva — examiners love seeing a live demo. 🚀
