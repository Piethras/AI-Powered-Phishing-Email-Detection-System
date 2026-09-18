# Day 17 — MySQL Integration

## What was built
- Installed MySQL Server locally (see mysql_password_reset_windows.md for
  a real troubleshooting sequence encountered along the way).
- Ran `backend/data/schema.sql` (written on Day 3) to create the actual
  `phishing_db` database with 4 tables: emails, predictions, whitelist,
  feedback.
- Added `app/models/db_models.py`: SQLAlchemy models matching the schema.
- Added `predict_and_save()` to `pipeline.py`: runs the full prediction
  pipeline AND persists results to MySQL (emails + predictions tables,
  correctly linked via foreign key).
- Updated `/api/predict` to use `predict_and_save()` instead of just
  returning an in-memory result.

## Verified working end-to-end
Live POST request to /api/predict correctly:
1. Ran the full 3-specialist + meta-classifier pipeline (Day 15/16)
2. Saved a new row to `emails` (sender, subject, body snippet, header_mismatch flag)
3. Saved a linked row to `predictions` (confidence_score, predicted_label, reasons, model_version)
Confirmed directly via SQL query - both tables show correctly populated,
correctly linked rows.

## Real issues encountered and resolved
- PyMySQL required the `cryptography` package for MySQL's default
  `caching_sha2_password` auth method (MySQL 8+/9.x) - not obvious from
  the error message alone until traced to its root cause.
- PowerShell's `Invoke-RestMethod` truncates long JSON responses by
  default in table view; `Format-List *` or accessing a specific
  property directly (`$response.email_id`) gives the full picture -
  worth remembering this isn't a backend bug, just a display quirk.

## Note for future cleanup
Test requests created duplicate rows in `emails`/`predictions` during
development - these should be cleared before any live demo (Day 20).