"""
Day 15 (continued) - Meta-classifier: combines text + header + URL
specialist outputs into one final decision. This directly addresses the
short-email/garbled-text failures from Day 14 - even when text is weak,
header/URL signals can still contribute.

Uses specialist_header_url.csv (CEAS_08 + SpamAssassin only, since these
are the only sources with all three feature types available together).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "parsers"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_score, recall_score
import joblib
from header_parser import analyze_sender
from url_checker import analyze_email_urls
from text_features import clean_text

df = pd.read_csv("../data/specialist_header_url.csv")

# Split FIRST (today's Day 12 lesson, still applies)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

text_vectorizer = joblib.load("../models/text_vectorizer.joblib")
text_clf = joblib.load("../models/text_classifier.joblib")
header_clf = joblib.load("../models/header_classifier.joblib")
url_clf = joblib.load("../models/url_classifier.joblib")

def get_specialist_scores(row_df):
    # Text specialist score
    cleaned = [clean_text(t) for t in row_df["body"].astype(str)]
    text_vec = text_vectorizer.transform(cleaned)
    text_scores = text_clf.predict_proba(text_vec)[:, 1]

    # Header specialist score
    header_feats = row_df["sender"].apply(lambda s: pd.Series({
        "header_mismatch": int(analyze_sender(str(s))["header_mismatch"]),
        "flag_count": len(analyze_sender(str(s))["flags"]),
        "display_name_len": len(analyze_sender(str(s))["display_name"] or ""),
        "domain_len": len(analyze_sender(str(s))["domain"] or ""),
    }))
    header_scores = header_clf.predict_proba(header_feats)[:, 1]

    # URL specialist score
    url_feats = row_df["body"].apply(lambda b: pd.Series({
        "url_count": analyze_email_urls(str(b))["url_count"],
        "suspicious_count": analyze_email_urls(str(b))["suspicious_count"],
        "has_suspicious": int(analyze_email_urls(str(b))["suspicious_count"] > 0),
    }))
    url_scores = url_clf.predict_proba(url_feats)[:, 1]

    return pd.DataFrame({
        "text_score": text_scores,
        "header_score": header_scores,
        "url_score": url_scores,
    })

print("Computing specialist scores for train set...")
meta_X_train = get_specialist_scores(train_df)
meta_y_train = train_df["label"].values

print("Computing specialist scores for test set...")
meta_X_test = get_specialist_scores(test_df)
meta_y_test = test_df["label"].values

meta_clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
meta_clf.fit(meta_X_train, meta_y_train)

y_pred = meta_clf.predict(meta_X_test)
print("\n=== META-CLASSIFIER RESULTS (combined text+header+url) ===")
print(classification_report(meta_y_test, y_pred, target_names=["legitimate", "phishing"]))

print("Feature importance (which specialist matters most):")
for name, importance in zip(meta_X_train.columns, meta_clf.feature_importances_):
    print(f"  {name}: {importance:.4f}")

joblib.dump(meta_clf, "../models/meta_classifier.joblib")
print("\nSaved meta_classifier.joblib")