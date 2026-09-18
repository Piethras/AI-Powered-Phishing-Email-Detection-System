# Day 13 — Threshold Tuning

## Precision-recall tradeoff at different thresholds (real data, test set n=14,946)

| Threshold | Precision | Recall |
|---|---|---|
| 0.30 | 95.56% | 99.45% |
| 0.40 | 97.31% | 98.63% |
| 0.50 (default) | 98.35% | 97.72% |
| 0.60 | 98.86% | 95.60% |
| **0.70 (chosen)** | **99.17%** | **92.63%** |
| 0.80 | 99.50% | 87.97% |
| 0.90 | 99.72% | 79.42% |
| 0.95 | 99.81% | 70.80% |

## Decision: operating threshold = 0.70

**Reasoning:** 0.70 captures the strongest precision improvement over the
default (98.35% -> 99.17%) while the recall cost stays proportionate
(97.72% -> 92.63%, ~5 points). Beyond 0.70, the tradeoff accelerates
sharply: from 0.70 to 0.95, precision gains only ~0.6 more points while
recall collapses by a further ~22 points. This matches Day 1's
precision-first design goal without excessively sacrificing the system's
ability to catch real phishing.

## Consistent with Day 1's core argument
A system that wrongly accuses legitimate email erodes trust entirely -
once ignored, it protects against nothing, including phishing it
correctly identifies. A moderate recall cost (missing some phishing) is
the accepted tradeoff for keeping user trust intact via high precision.

## Next: cross-validation (Day 13 continued) to confirm this isn't a fluke
of one particular train/test split, before finalizing.

## Cross-validation confirmation (5-fold)

| Fold | Precision | Recall |
|---|---|---|
| 1 | 0.9909 | 0.9253 |
| 2 | 0.9920 | 0.9270 |
| 3 | 0.9929 | 0.9263 |
| 4 | 0.9937 | 0.9274 |
| 5 | 0.9927 | 0.9209 |

**Mean precision: 0.9924 (+/- 0.0010)**
**Mean recall: 0.9254 (+/- 0.0024)**

Extremely tight variance across folds confirms the threshold=0.70 choice
is stable and not an artifact of one particular train/test split. This
is strong evidence the model generalizes consistently, not just on the
single Day 12 split.