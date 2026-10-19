# AI-Powered Spam Email Detection and Explainable Threat Analysis System

Advanced B.Tech project combining NLP, supervised machine learning, explainability-oriented feature analysis, cybersecurity heuristics, FastAPI and React.

## Architecture

User → React Dashboard → FastAPI → NLP preprocessing + feature extraction → ML model → prediction + confidence → security indicators → risk score → SQLite history.

## Included ML pipeline

- Word TF-IDF n-grams
- Character TF-IDF n-grams
- Structural/security features
- Logistic Regression
- Multinomial Naive Bayes
- Calibrated Linear SVM
- Random Forest
- Stratified holdout evaluation + 3-fold CV F1
- Accuracy, precision, recall, F1, ROC-AUC, confusion matrix

## Quick start

### 🚀 One-Command Launch (Backend + Frontend together)
From the project root directory, run:
```powershell
python run.py
```
*(Or double-click `run.bat` on Windows)*

This single command will:
1. Start the FastAPI backend on port 8000.
2. Start the Vite React frontend on port 5173.
3. Automatically open your web browser to `http://localhost:5173`.
4. Allow you to cleanly stop both services anytime with `Ctrl + C`.

---

### Manual Launch (Separate Terminals)

#### 1. Backend (Terminal 1)
```powershell
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

#### 2. Frontend (Terminal 2)
```powershell
cd frontend
npm install
npm run dev
```

## Dataset

A small seed dataset is included only so the project runs immediately. For meaningful academic evaluation, replace `data/raw/emails.csv` with a properly sourced public spam dataset. Required columns: a text/message/body/email column and a label/class/category column. Do not present seed-dataset metrics as production performance.

## API

- POST `/api/analyze`
- POST `/api/analyze-eml`
- GET `/api/history`
- GET `/api/dashboard`
- GET `/api/model-info`
- POST `/api/train`
- GET `/api/health`

## Security notes

Uploaded EML files are parsed as untrusted data. Attachments are never executed and extracted URLs are never visited automatically. URL indicators are heuristic and do not prove maliciousness.
