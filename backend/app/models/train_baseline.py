"""
Day 12 - Train baseline Random Forest classifiers (text specialist first).

Critical: split BEFORE fitting TF-IDF, to avoid the train/test leakage
discussed today. The vectorizer is fit ONLY on training text, then applied
(never re-fit) to the test text.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)
from text_features import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# --- Load data ---
df = pd.read_csv("../data/specialist_text.csv")
print(f"Loaded {len(df)} rows")

# --- Split FIRST, before any fitting (today's core lesson) ---
X_train_text, X_test_text, y_train, y_test, src_train, src_test = train_test_split(
    df["text"], df["label"], df["source"],
    test_size=0.2, random_state=42, stratify=df["label"]
)
print(f"Train: {len(X_train_text)}  Test: {len(X_test_text)}")

# --- Fit TF-IDF ONLY on training text ---
cleaned_train = [clean_text(t) for t in X_train_text]
cleaned_test = [clean_text(t) for t in X_test_text]

vectorizer = TfidfVectorizer(max_features=3000, stop_words="english", ngram_range=(1, 2))
X_train = vectorizer.fit_transform(cleaned_train)   # fit_transform on TRAIN only
X_test = vectorizer.transform(cleaned_test)          # transform only on TEST - no re-fitting

# --- Train Random Forest ---
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

# --- Evaluate ---
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]

print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=["legitimate", "phishing"]))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

# --- Day 12 action item from Day 7: per-source breakdown ---
print("\n=== Per-source accuracy (Day 7 follow-up: does source affect results?) ===")
results_df = pd.DataFrame({"y_true": y_test, "y_pred": y_pred, "source": src_test})
for source in results_df["source"].unique():
    subset = results_df[results_df["source"] == source]
    acc = (subset["y_true"] == subset["y_pred"]).mean()
    print(f"  {source}: {len(subset)} rows, accuracy = {acc:.4f}")

# --- More precise test: false positive rate on LEGITIMATE emails, by source ---
print("\n=== False positive rate on LEGITIMATE emails, by source (Day 7 concern) ===")
legit_only = results_df[results_df["y_true"] == 0]
for source in legit_only["source"].unique():
    subset = legit_only[legit_only["source"] == source]
    false_positive_rate = (subset["y_pred"] == 1).mean()
    print(f"  {source}: {len(subset)} legitimate emails, {false_positive_rate*100:.2f}% wrongly flagged as phishing")

# --- Save model + vectorizer for later use ---
os.makedirs("../models", exist_ok=True)
joblib.dump(clf, "../models/text_classifier.joblib")
joblib.dump(vectorizer, "../models/text_vectorizer.joblib")
print("\nSaved model and vectorizer to backend/models/")