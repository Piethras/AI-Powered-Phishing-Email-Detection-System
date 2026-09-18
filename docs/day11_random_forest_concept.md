# Day 11 — Random Forest Concept (in progress)

## Decision tree splitting (Gini impurity) - hand-calculated
- header_mismatch split: weighted Gini = 0.2 (purer)
- url_suspicious split: weighted Gini = 0.375
- Tree picks header_mismatch first (lower Gini = purer split)

## Random Forest = many trees + bagging + feature randomness
Each tree sees a random subset of rows and features. A spurious pattern
(e.g. Day 7's "enron" leakage) only strongly affects trees that happened
to see it; other trees rely on more general signals. Majority vote is
more robust than one tree trained on everything.

## Feature importance (to continue next session)
header_mismatch likely has higher importance than url_suspicious, since
it produced a purer split. This will power the dashboard's "why flagged" feature.
Finish feature importance, build tree diagram.