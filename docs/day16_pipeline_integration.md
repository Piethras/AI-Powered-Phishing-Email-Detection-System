# Day 16 — Flask Pipeline Integration

## What was built
- `app/api/pipeline.py`: loads all 5 trained models once at startup,
  runs the full pipeline (parser -> 3 specialists -> meta-classifier)
  for a single email.
- `/api/predict` endpoint wired to use this pipeline for real.

## First live end-to-end test
Input: sender="security@paypa1-secure.ru" (bare address, no display name),
body containing urgency language + lookalike-domain URL.

Result: final_score=0.98, label=phishing (correct)
- text_score: 0.9398 (urgency language correctly caught)
- url_score: 0.7038 (suspicious URL correctly caught)
- header_score: 0.4042 (lower than expected)

## Investigation: why was header_score lower than expected?
Traced directly: `analyze_sender()` on a BARE address (no display name)
correctly returns header_mismatch=False, since the brand-mismatch check
(Day 4) specifically looks for a brand name in the display name field.
Confirmed by re-testing with a properly formatted sender string
('"PayPal Support" <security@paypa1-secure.ru>') - header_mismatch
correctly returned True with both expected flags.

## Honest limitation identified (not a bug)
The header specialist's brand-impersonation check requires a display
name to be present. An attacker sending phishing mail with no display
name (or a generic one) bypasses this specific check - though the
system's overall design (text + URL specialists) still caught this
example correctly (final score 0.98), demonstrating the value of the
ensemble architecture even when one specialist has a blind spot.

## Confirmed working end-to-end
Raw input -> Flask /api/predict -> parser -> 3 specialists -> 
meta-classifier -> final JSON response, all live, matching the exact
pipeline traced through in Day 3/15 discussions.