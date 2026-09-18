# Day 15 — Specialist Ensemble: Final Results

## Individual specialist performance (test set, n=8,993 from CEAS_08+SpamAssassin)

| Specialist | Precision (avg) | Recall (avg) | Notes |
|---|---|---|---|
| Text (TF-IDF+RF) | 98% | 98% | Strong alone (trained on 74,730 rows, all sources) |
| Header | 70% | 70% | Weak alone - header_mismatch rarely fires (Day 4: <0.2%) |
| URL | 72-78% | 46-96% (class-dependent) | Weak/imbalanced alone - sparse features |

## Meta-classifier (combined) performance

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Legitimate | 0.99 | 0.99 | 0.99 |
| Phishing | 0.99 | 0.99 | 0.99 |

**The combined ensemble outperformed even the strongest individual
specialist (text, 98%)**, despite the other two specialists being
individually weak (70-72%). This confirms the Day 9 architecture decision:
weak, independent signals can still add real value when combined, since
the meta-classifier learns appropriate trust weighting rather than
requiring every component to be strong alone.

## Meta-classifier feature importance
- text_score: 78.54%
- header_score: 11.29%
- url_score: 10.16%

The meta-classifier learned, without being told, to weight the text
specialist far more heavily - consistent with it being individually the
strongest signal. This mirrors the Day 11 feature-importance mechanism,
now operating one level up (specialist importance, not word importance).

## Connection to Day 14 error analysis
This ensemble directly targets the short-email blind spot identified on
Day 14: an email with too little text for the text specialist to work
with can still be evaluated on header and URL signals, which don't
depend on body text length or content quality at all.

## Final model choice
**Primary system: text specialist (98% alone) + header specialist (70%)
+ URL specialist (72-78%) combined via Random Forest meta-classifier
(99% combined)**, operating at the Day 13 threshold philosophy (tunable
per deployment need). This is the architecture carried into Week 4
(Flask/API integration).

## Saved artifacts
`header_classifier.joblib`, `url_classifier.joblib`, `meta_classifier.joblib`
(plus Day 12's `text_classifier.joblib`, `text_vectorizer.joblib`)