# PhishGuard — AI-Powered Phishing Email Detection System

An email classifier that scans incoming emails for phishing indicators
— suspicious sender addresses, malicious URLs, and manipulative
language patterns — and combines them into a single, explainable
confidence score. Built to prioritize **precision**: minimizing false
alarms on legitimate email is treated as more important than catching
every possible phishing attempt, so the system stays trustworthy
enough that its warnings are actually acted on.

## Live features
- **Upload or paste an email** and get an instant score, with the
  specific reasons behind it (not just a number).
- **Confidence Score Dashboard**: live stats, a detection trend chart,
  a flagged-rate breakdown, and the most frequently flagged sender
  domains — all computed from real stored data, not placeholders.
- **Full email history**, filterable by outcome.
- **Feedback loop**: mark a result as correct or incorrect; feedback is
  logged for human review, not automatically applied to the model.
- **Whitelist**: explicitly trust a sender domain, with a full audit
  trail (who added it, when).
- **"Needs Review" status**: when the text model doesn't recognize
  enough of an email's content to trust its own score (e.g. non-English
  text), the system says so instead of guessing.

## Architecture

Raw email
-> Parser (headers, body, URLs)
-> 3 independent specialists (text / header / URL), each producing a score
-> Meta-classifier combines the 3 scores into one final verdict
-> Flask API persists the result to MySQL
-> React dashboard displays it, live


Three specialists were trained separately (rather than one combined
model) because the available training data did not consistently
provide header and URL fields across all sources — training one model
on inconsistently-available features would have taught it a false
shortcut. See `docs/day9_architecture_decision.md` for the full
reasoning.

## Model performance (validated, Day 12–15)
- Text specialist (TF-IDF + Random Forest): 98% precision / 98% recall
- Full ensemble (text + header + URL + meta-classifier): 99% precision
  / 99% recall
- Operating threshold: 0.70, chosen via a precision-recall tradeoff
  analysis and confirmed stable with 5-fold cross-validation
  (mean precision 99.24% ± 0.10%)

## Tech stack
- **Backend**: Python, Flask, SQLAlchemy
- **ML**: scikit-learn (TF-IDF, Random Forest), pandas
- **Database**: MySQL
- **Frontend**: React (Vite), Recharts, lucide-react

## Project structure

backend/
app/
api/ Flask routes and the prediction pipeline
parsers/ Email header/body parsing
features/ URL checking, TF-IDF, keyword/coverage guards
models/ Trained model files (.joblib) and DB models
data/ Schema + datasets (not committed - see .gitignore)
frontend/
src/
components/ Reusable UI pieces
pages/ Route-level pages
docs/ Day-by-day findings, decisions, and writeups
notebooks/ Data exploration notebook


## Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```
Create a `.env` file in `backend/`:

DATABASE_URL=mysql+pymysql://root:YOURPASSWORD@localhost/phishing_db

Create the database:
```bash
mysql -u root -p < data/schema.sql
```
Run the server:
```bash
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open the printed local URL (typically `http://localhost:5173`).

## Known limitations (documented, not hidden)
- **Non-English text**: the text specialist is trained on English data
  only. A lightweight, rule-based phrase check and a "text coverage"
  guard (which returns "needs review" instead of a false-confidence
  score) partially cover this gap for French, but this is not a
  general multilingual solution. See `docs/day22...` notes.
- **Very short or heavily obfuscated emails**: the text specialist has
  limited signal on very sparse or intentionally garbled content; the
  header/URL specialists partly compensate (see `docs/day14_error_analysis.md`).
- **No authentication**: intentionally out of scope for this academic
  prototype (see `docs/privacy_and_security.md` for the full reasoning
  and what production deployment would require).
- **Responsive layout**: a CSS grid sizing issue affects some
  intermediate/laptop viewport widths; desktop and mobile (hamburger
  nav) both render correctly.

## Data & privacy
See `docs/privacy_and_security.md` for what is stored, what is not
implemented, and the system's intended scope.

## Datasets
Trained on a combination of the Enron, CEAS_08, and SpamAssassin
public research corpora, deliberately assembled with known, auditable
composition after identifying that a pre-mixed alternative dataset's
composition could not be verified (see `docs/day7_tfidf_results.md`).