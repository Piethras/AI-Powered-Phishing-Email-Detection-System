# AI-Powered Phishing Email Detection System
## 4-Week Project Plan (20 working days)

**Goal:** Build a defensible, well-understood, end-to-end phishing detection system — not just a working script, but a project you can explain and justify at every layer.

**Guiding principle for every day:** understand the *why* before the *how*. Every build day is preceded by a concept day. Every module ends with "could I explain this to a panel?"

---

## WEEK 1 — Foundations: Domain, Data, and Environment

### Day 1 (Today) — Domain Understanding ✅ started
- [x] The accuracy paradox on imbalanced data
- [x] Precision vs. Recall — definitions, confusion matrix, worked examples
- [x] Why this project prioritizes precision over recall (trust argument)
- [x] Raw email anatomy: headers vs. body
- [x] Why `Received:` is harder to spoof than `From:`
- [ ] SPF / DKIM / DMARC — what they are, why they matter (mini-lesson)
- **Deliverable:** One-page personal notes summarizing precision/recall tradeoff in your own words (defense material)

### Day 2 — Data Understanding ✅ COMPLETE
- [x] Inspected structure of 5/7 source files (Enron, Nazario, CEAS_08, SpamAssassin, phishing_email combined)
- [x] Class balance checked per source — visualized in `class_balance.png`
- [x] **Real leakage risk found and resolved**: Nazario.csv is 100% phishing with header/URL fields; text-only sources (Enron, phishing_email) have both classes but no headers. Resolved by assigning each module its own appropriate data source (see notebook §4)
- [x] Data quality issue found: invalid dates (e.g. year 2100) in CEAS_08 — decided against using raw dates as a feature
- [x] Ethical/legal note written — public research datasets only, no live inbox scraping
- [x] **Deliverable produced:** `notebooks/day2_data_understanding.ipynb` (executed, with class balance chart and 5+5 sample inspection)
- **Pending, low priority:** inspect `Ling.csv` and `Nigerian_Fraud.csv` structure (doesn't block Day 3 — data strategy is already resolved without them)

### Day 3 — Environment & Architecture Setup ✅ COMPLETE
- [x] Reasoned through the full data flow independently before building anything (parser → 3 modules → classifier → Flask → MySQL/React → feedback loop)
- [x] System architecture diagram built and saved (`docs/architecture_notes.md` + rendered diagram)
- [x] Repo structure created: backend/(app/parsers, app/features, app/api, models, data), frontend/, notebooks/, docs/, data/
- [x] Flask skeleton built AND tested — `/api/health` and `/api/predict` confirmed working via test client
- [x] MySQL schema drafted (`backend/data/schema.sql`): emails, predictions, whitelist, feedback tables
- [x] React (Vite) skeleton created — placeholder component that pings the Flask health endpoint
- [x] Understood *why* this is a 3-tier architecture (separation of concerns: MySQL=persistence, Flask=orchestration/logic, React=presentation) — defense-ready explanation
- **Deliverable:** `day3_project_skeleton.zip` — working repo skeleton + architecture notes

### Day 4 — Module 1: Email Header & Body Parser ✅ COMPLETE
- [x] Built `parse_raw_email()` using Python's `email` package for genuine raw `.eml`/MIME input — validated it correctly reassembles folded headers and captures ALL `Received:` hops (not just one)
- [x] Built `analyze_sender()` for the "Display Name <address>" format our labeled datasets provide — 3 heuristics: brand/domain mismatch, org-claim-on-free-webmail, lookalike domain digits
- [x] Wrote a formal test suite (`tests/test_header_parser.py`) — 8/8 tests passing, including edge cases (folded headers, multi-hop chains, malformed input)
- [x] Evaluated at full scale on CEAS_08 (n=39,154) and SpamAssassin (n=5,809): false-positive rate <0.2% on both, confirming high precision; true-positive rate <0.1%, revealing this signal alone has low recall on this corpus (dominated by generic spam, not brand impersonation)
- [x] Documented an honest limitation: dataset lacks full `Received:` chains, so chain-based spoofing detection is implemented and validated synthetically but not statistically evaluated at scale
- **Deliverable:** `header_parser.py`, `test_header_parser.py`, `day4_header_module_results.md`

### Day 5 — Module 2: URL Extraction & Reputation Check + Week 1 Checkpoint ✅ COMPLETE
- [x] Built two-path URL extraction: plain-text regex (matches our dataset's actual format) + real HTML `<a href>` parsing (production path)
- [x] Built standalone heuristics (no API needed): IP-literal domains, known shorteners, long domains, excessive hyphens, malformed URL structure
- [x] Built anchor-text-vs-href mismatch detection, validated on synthetic HTML (dataset doesn't contain real HTML, same limitation pattern as Day 4)
- [x] **Real debugging cycle, evidence-based**: found and fixed a genuine bug (`urlparse` swallowing malformed query strings into the domain), then correctly demoted two signals (shorteners, malformed structure) from "standalone suspicious" to "weak/logged" after evidence showed they fire on both classes
- [x] Identified and documented a dataset artifact (`127.0.0.1:631`, an IPP/CUPS leftover from collection) rather than chasing it with more code
- [x] Full-scale evaluation: 0.18% false positive rate (legit), 0.04% true positive rate (phishing), consistent with Day 4's "narrow, high-precision, complementary signal" pattern
- **Week 1 Checkpoint met:** ran the actual system on your own machine end-to-end (venv, tests, Flask server), debugged a real bug independently with guidance, and can explain why weak signals shouldn't drive standalone flags
- **Deliverable:** `url_checker.py`, `test_url_checker_real_data.py`, `debug_url_flags.py`, `day5_url_module_results.md`

---

## WEEK 2 — Feature Engineering: Turning Emails into Numbers

### Day 6 — NLP Concept Deep Dive: TF-IDF ✅ COMPLETE
- [x] Built TF-IDF intuition from scratch: rarity + frequency, worked by hand on a 3-sentence toy example (verify: TF=0.167, IDF=1.099, TF-IDF=0.183 — vs. "to": TF-IDF=0.029)
- [x] Understood why BOTH TF and IDF are needed (Email A vs Email B intensity example)
- [x] Understood why common words get automatically suppressed (near-zero IDF), without manual stopword lists
- **Deliverable:** Hand-calculated worked example (documented in conversation, defense-ready)

### Day 7 — Build TF-IDF Pipeline ✅ COMPLETE (with a real, documented detour)
- [x] Built `text_features.py`: `clean_text()`, `build_tfidf_features()`, `top_terms_by_class()` — validated against toy sentences, matched hand-calculated Day 6 results exactly
- [x] **Major finding #1:** discovered `phishing_email.csv`'s source composition is unverifiable (fingerprint-matching against source files failed, ~0-4% overlap even on visibly identical content) — decided to build our OWN training set (`training_set.csv`, 74,730 rows) from Enron + CEAS_08 + SpamAssassin with full, auditable composition (`source` column preserved)
- [x] **Major finding #2:** diversifying legitimate sources did NOT remove "enron" as the top legitimate TF-IDF term — correctly diagnosed root cause via IDF math (adding documents that lack a word doesn't dilute that word's rarity)
- [x] **Major finding #3:** inspected Enron's spam-labeled rows directly — confirmed our "phishing" class spans generic spam to targeted phishing, an honest dataset scoping limitation
- [x] Considered and correctly rejected word-blocklisting (same fragility as Day 5's malformed-URL lesson) in favor of deferred, evidence-based testing
- **Deliverable:** `text_features.py`, `build_training_set.py`, `training_set.csv`, `day7_tfidf_results.md`
- **Action item carried to Day 12:** evaluate classifier metrics BY SOURCE to test whether Enron vocabulary reliance causes real misclassification of non-Enron legitimate mail

### Day 8 — NLP Concept Deep Dive: BERT (and why/whether to use it)
- Concept: contextual embeddings vs. TF-IDF's "bag of words"
- Why BERT *could* catch phishing that varies its wording while keeping the same intent
- Honest cost discussion: compute cost, complexity, diminishing returns for a portfolio project
- **Decision point:** commit to TF-IDF+RF as the primary system; BERT becomes a documented stretch goal/comparison, not a blocker
- **Deliverable:** One paragraph in report justifying this choice (this is a common defense question — "why not just use the fanciest model?")

### Day 9 — Combining Structured + Text Features
- Concept: why header/URL flags (structured features) + TF-IDF (text features) together outperform either alone
- Build unified feature matrix: [TF-IDF vector] + [domain mismatch flag] + [URL reputation flag] + [urgency keyword count] + [attachment type flag]
- **Deliverable:** `build_features.py` producing final training-ready feature matrix

### Day 10 — Week 2 Checkpoint
- Review: can you explain TF-IDF math, and why we combined feature types instead of using text alone?
- Sanity-check the feature matrix for leakage or obviously broken columns
- **Deliverable:** Clean, saved feature matrix (train/test split done and saved) ready for modeling

---

## WEEK 3 — Modeling: Training, Evaluating, Defending Choices

### Day 11 — Concept Deep Dive: Random Forest
- How a single decision tree splits data (Gini impurity / entropy, explained simply)
- How Random Forest combines many trees (bagging + feature randomness) to reduce overfitting
- Why RF gives you feature importance — a big win for explainability in a security dashboard
- **Deliverable:** Hand-drawn/simple diagram of one decision tree split on 2 features (defense visual)

### Day 12 — Train Baseline Model + Initial Evaluation
- Train Random Forest on the Week 2 feature matrix
- Generate confusion matrix, precision, recall, F1, ROC-AUC on test set
- **Deliverable:** First model results report — baseline numbers, honestly recorded (even if not great yet)

### Day 13 — Threshold Tuning for Precision
- Concept: decision threshold — how moving it shifts precision/recall tradeoff (ties directly back to Day 1)
- Plot precision-recall curve, choose an operating threshold that satisfies "high precision" requirement
- Cross-validation to confirm the choice isn't a fluke of one train/test split
- **Deliverable:** Precision-recall curve chart + justified threshold choice (key report figure)

### Day 14 — Error Analysis + Stretch: LSTM/BERT Comparison
- Manually inspect false positives and false negatives — what patterns is the model missing/over-flagging?
- If time allows: quick BERT or LSTM comparison run, documented honestly (better, worse, or not worth the cost?)
- **Deliverable:** Error analysis notes — this is gold for your defense ("here's what we got wrong and why")

### Day 15 — Week 3 Checkpoint: Finalize Model
- Lock in final model + threshold + feature set
- Save trained model (pickle/joblib) for API integration
- **Checkpoint:** Can you defend every modeling choice — why RF, why this threshold, what the error analysis revealed?
- **Deliverable:** Final trained model file + one-page model card (metrics, tradeoffs, limitations)

---

## WEEK 4 — System Integration: Making It a Real Product

### Day 16 — Flask Backend API
- Design endpoints: `/predict` (score an email), `/history`, `/whitelist`, `/feedback`
- Wrap the saved model in a Flask service
- **Deliverable:** Working API — POST an email, get back a phishing score + flagged reasons

### Day 17 — MySQL Integration
- Implement schema from Day 3: store predictions, confidence scores, whitelist entries, feedback
- Connect Flask to MySQL (SQLAlchemy or raw connector)
- **Deliverable:** API writes/reads real data to/from MySQL

### Day 18 — React Dashboard
- Build the Confidence Score Dashboard: list of flagged emails, score, and *why* it was flagged (feature-based explanation, using RF feature importances)
- **Deliverable:** Working frontend showing live predictions from the backend

### Day 19 — Whitelist & Feedback Loop
- Implement "mark as safe" / "this was missed" actions from the dashboard
- Wire feedback into whitelist logic (and note, for the report, how it *could* feed retraining even if full retraining automation is out of scope)
- **Deliverable:** End-to-end demo: raw email in → parsed → scored → shown on dashboard → user gives feedback → stored

### Day 20 — Final Polish & Defense Preparation
- Full system test: run 10 unseen emails through the whole pipeline live
  - **Note:** export a few real personal emails as `.eml` here (Gmail: "Download message"; Outlook: drag-to-desktop or use Outlook web) and run them through `parse_raw_email()` + the full pipeline as a live, non-synthetic demo moment
- Write/finalize README, architecture diagram, model card, limitations section
- Prepare defense materials: anticipated questions (why precision over recall, why RF over LSTM, how headers are parsed, what the accuracy paradox is, system architecture walkthrough)
- **Deliverable:** Complete, demoable system + defense Q&A prep sheet

---

## Standing rules for the whole project

1. **No day starts with code before the concept is explainable out loud.**
2. **Every module gets a short "why we built it this way" note** — these become your report/defense content, written as we go, not scrambled together at the end.
3. **Checkpoints are non-negotiable.** If a checkpoint isn't met, we spend extra time there before moving forward — better to slip a day than defend something you don't understand.
4. **Keep all metrics honest**, including bad ones. A documented weakness you understand beats a suspiciously perfect number you can't explain.

---

## Progress Tracker

| Week | Focus | Status |
|---|---|---|
| Week 1 | Foundations: domain, data, env, parser, URL module | ✅ Complete (Days 1-5) — Week 2 starts next |
| Week 2 | Feature engineering: TF-IDF, BERT concept, combined features | 🔵 In progress (Days 6-7 done, Day 8 next) |
| Week 3 | Modeling: Random Forest, tuning, evaluation, error analysis | ⬜ Not started |
| Week 4 | Integration: Flask, MySQL, React, feedback loop, defense prep | ⬜ Not started |
