"""
Day 15 (continued) - Train the Header specialist, using engineered
features from header_parser.py on specialist_header_url.csv (CEAS_08 +
SpamAssassin only - the sources with real sender data).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "parsers"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from header_parser import analyze_sender

df = pd.read_csv("../data/specialist_header_url.csv")

def to_features(sender):
    r = analyze_sender(str(sender))
    return pd.Series({
        "header_mismatch": int(r["header_mismatch"]),
        "flag_count": len(r["flags"]),
        "display_name_len": len(r["display_name"] or ""),
        "domain_len": len(r["domain"] or ""),
    })

X = df["sender"].apply(to_features)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

print(classification_report(y_test, clf.predict(X_test), target_names=["legitimate", "phishing"]))

os.makedirs("../models", exist_ok=True)
joblib.dump(clf, "../models/header_classifier.joblib")
print("Saved header_classifier.joblib")