"""
Day 14 - Error analysis at threshold=0.70. Look at actual misclassified
emails, not just aggregate metrics, to find real patterns in the model's
blind spots.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import pandas as pd
from sklearn.model_selection import train_test_split
from text_features import clean_text
import joblib

df = pd.read_csv("../data/specialist_text.csv")
X_train_text, X_test_text, y_train, y_test, src_train, src_test = train_test_split(
    df["text"], df["label"], df["source"],
    test_size=0.2, random_state=42, stratify=df["label"]
)

vectorizer = joblib.load("../models/text_vectorizer.joblib")
clf = joblib.load("../models/text_classifier.joblib")

cleaned_test = [clean_text(t) for t in X_test_text]
X_test = vectorizer.transform(cleaned_test)
y_proba = clf.predict_proba(X_test)[:, 1]

THRESHOLD = 0.70
y_pred = (y_proba >= THRESHOLD).astype(int)

results = pd.DataFrame({
    "text": X_test_text.values,
    "y_true": y_test.values,
    "y_pred": y_pred,
    "proba": y_proba,
    "source": src_test.values,
})

false_positives = results[(results["y_true"] == 0) & (results["y_pred"] == 1)]
false_negatives = results[(results["y_true"] == 1) & (results["y_pred"] == 0)]

print(f"Total false positives (legit called phishing): {len(false_positives)}")
print(f"Total false negatives (phishing called legit): {len(false_negatives)}")

print("\n=== FALSE POSITIVES (legit wrongly flagged) - 10 examples ===")
for i, row in false_positives.sort_values("proba", ascending=False).head(10).iterrows():
    print(f"[source={row['source']}, confidence={row['proba']:.2f}]")
    print(" ", row["text"][:150].replace("\n", " "))
    print("---")

print("\n=== FALSE NEGATIVES (phishing that slipped through) - 10 examples ===")
for i, row in false_negatives.sort_values("proba", ascending=True).head(10).iterrows():
    print(f"[source={row['source']}, confidence={row['proba']:.2f}]")
    print(" ", row["text"][:150].replace("\n", " "))
    print("---")