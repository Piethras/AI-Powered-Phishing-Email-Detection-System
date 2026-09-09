"""
Day 13 - Threshold tuning: find a threshold that pushes precision higher,
consistent with Day 1's precision-first design goal, while measuring the
recall cost honestly.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, precision_score, recall_score
from text_features import clean_text
import joblib

# Reload the same split as Day 12 (same random_state = same split)
df = pd.read_csv("../data/specialist_text.csv")
X_train_text, X_test_text, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

vectorizer = joblib.load("../models/text_vectorizer.joblib")
clf = joblib.load("../models/text_classifier.joblib")

cleaned_test = [clean_text(t) for t in X_test_text]
X_test = vectorizer.transform(cleaned_test)
y_proba = clf.predict_proba(X_test)[:, 1]

# Compute precision/recall at every possible threshold
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)

print("threshold | precision | recall")
for t in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
    y_pred_at_t = (y_proba >= t).astype(int)
    p = precision_score(y_test, y_pred_at_t)
    r = recall_score(y_test, y_pred_at_t)
    print(f"  {t:.2f}    |   {p:.4f}  | {r:.4f}")

# --- Cross-validation: confirm threshold=0.70 isn't a fluke of one split ---
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

print("\n=== 5-fold cross-validation at threshold=0.70 ===")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
X_all = df["text"].values
y_all = df["label"].values

fold_precisions, fold_recalls = [], []
for fold, (train_idx, test_idx) in enumerate(skf.split(X_all, y_all)):
    X_tr, X_te = X_all[train_idx], X_all[test_idx]
    y_tr, y_te = y_all[train_idx], y_all[test_idx]

    cleaned_tr = [clean_text(t) for t in X_tr]
    cleaned_te = [clean_text(t) for t in X_te]

    vec = TfidfVectorizer(max_features=3000, stop_words="english", ngram_range=(1, 2))
    Xtr_vec = vec.fit_transform(cleaned_tr)
    Xte_vec = vec.transform(cleaned_te)

    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(Xtr_vec, y_tr)

    proba = model.predict_proba(Xte_vec)[:, 1]
    pred_at_07 = (proba >= 0.70).astype(int)

    p = precision_score(y_te, pred_at_07)
    r = recall_score(y_te, pred_at_07)
    fold_precisions.append(p)
    fold_recalls.append(r)
    print(f"  Fold {fold+1}: precision={p:.4f}, recall={r:.4f}")

print(f"\nMean precision: {np.mean(fold_precisions):.4f} (+/- {np.std(fold_precisions):.4f})")
print(f"Mean recall:    {np.mean(fold_recalls):.4f} (+/- {np.std(fold_recalls):.4f})")