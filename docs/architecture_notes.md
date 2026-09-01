# System Architecture — Day 3

## Data flow (reasoned through, not just diagrammed)

1. Raw email (.eml) arrives
2. Header & Body Parser splits it into: headers, body text, URLs
3. Three modules analyze their piece in parallel:
   - Header check (From vs Received domain mismatch, spoofing indicators)
   - URL reputation (VirusTotal lookup, homoglyph/shortener heuristics)
   - NLP features (TF-IDF / BERT on body text)
4. Random Forest classifier combines all features into one confidence score
5. Flask API orchestrates the above and:
   - Persists the result to MySQL (emails, predictions tables)
   - Serves the result to the React dashboard on request
6. User views flagged emails + reasons on the React dashboard
7. User feedback ("false positive" / "missed phishing") is submitted back
   through Flask into MySQL (feedback, whitelist tables) — closing the loop

## Why this is a 3-tier architecture (defense point)

- **MySQL** — persistence only. Stores data, computes nothing.
- **Flask** — orchestration + business logic. Runs the ML pipeline, keeps
  secrets (VirusTotal API key) server-side, never exposed to the browser.
- **React** — presentation only. Renders what Flask gives it; makes no
  decisions of its own.

This separation of concerns means each layer can be modified, tested, or
swapped independently — e.g., the classifier can be upgraded (RF -> LSTM)
without touching React at all.
