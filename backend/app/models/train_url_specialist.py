"""
Day 15 (continued) - Train the URL specialist using url_checker.py
features on specialist_header_url.csv.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from url_checker import analyze_email_urls

df = pd.read_csv("../data/specialist_header_url.csv")

def to_features(body):
    r = analyze_email_urls(str(body))
    return pd.Series({
        "url_count": r["url_count"],
        "suspicious_count": r["suspicious_count"],
        "has_suspicious": int(r["suspicious_count"] > 0),
    })

X = df["body"].apply(to_features)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

print(classification_report(y_test, clf.predict(X_test), target_names=["legitimate", "phishing"]))

os.makedirs("../models", exist_ok=True)
joblib.dump(clf, "../models/url_classifier.joblib")
print("Saved url_classifier.joblib")