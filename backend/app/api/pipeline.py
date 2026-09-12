"""
The full prediction pipeline (Day 16): raw email -> parser -> 3 specialists
-> meta-classifier -> final result. Loads all 5 trained models once at
import time (not per-request) for performance.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "parsers"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "features"))

import joblib
import pandas as pd
from header_parser import analyze_sender, parse_raw_email
from url_checker import analyze_email_urls
from text_features import clean_text

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

# Load once, at startup - not on every request
text_vectorizer = joblib.load(os.path.join(MODELS_DIR, "text_vectorizer.joblib"))
text_clf = joblib.load(os.path.join(MODELS_DIR, "text_classifier.joblib"))
header_clf = joblib.load(os.path.join(MODELS_DIR, "header_classifier.joblib"))
url_clf = joblib.load(os.path.join(MODELS_DIR, "url_classifier.joblib"))
meta_clf = joblib.load(os.path.join(MODELS_DIR, "meta_classifier.joblib"))

THRESHOLD = 0.70  # Day 13's chosen operating threshold


def predict_email(sender: str, body: str) -> dict:
    """
    Runs the full pipeline on a single email and returns the final
    result, matching the reasoning traced through in conversation:
    parser -> 3 specialists -> meta-classifier -> final decision.
    """
    # --- Text specialist ---
    cleaned = clean_text(body)
    text_vec = text_vectorizer.transform([cleaned])
    text_score = text_clf.predict_proba(text_vec)[0, 1]

    # --- Header specialist ---
    header_result = analyze_sender(sender)
    header_feats = pd.DataFrame([{
        "header_mismatch": int(header_result["header_mismatch"]),
        "flag_count": len(header_result["flags"]),
        "display_name_len": len(header_result["display_name"] or ""),
        "domain_len": len(header_result["domain"] or ""),
    }])
    header_score = header_clf.predict_proba(header_feats)[0, 1]

    # --- URL specialist ---
    url_result = analyze_email_urls(body)
    url_feats = pd.DataFrame([{
        "url_count": url_result["url_count"],
        "suspicious_count": url_result["suspicious_count"],
        "has_suspicious": int(url_result["suspicious_count"] > 0),
    }])
    url_score = url_clf.predict_proba(url_feats)[0, 1]

    # --- Meta-classifier: combine all 3 scores into final decision ---
    meta_input = pd.DataFrame([{
        "text_score": text_score,
        "header_score": header_score,
        "url_score": url_score,
    }])
    final_score = meta_clf.predict_proba(meta_input)[0, 1]
    final_label = "phishing" if final_score >= THRESHOLD else "legitimate"

    # Build "reasons" for the dashboard (Day 3 requirement) from whichever
    # specialist(s) contributed most
    reasons = []
    if header_result["flags"]:
        reasons.extend(header_result["flags"])
    if url_result["suspicious_count"] > 0:
        reasons.append(f"{url_result['suspicious_count']} suspicious URL(s) found")
    if not reasons and final_label == "phishing":
        reasons.append("flagged primarily on email text/language patterns")

    return {
        "final_score": round(float(final_score), 4),
        "label": final_label,
        "threshold_used": THRESHOLD,
        "specialist_scores": {
            "text": round(float(text_score), 4),
            "header": round(float(header_score), 4),
            "url": round(float(url_score), 4),
        },
        "reasons": reasons,
    }

def predict_and_save(sender: str, body: str, subject: str = ""):
    """
    Runs the pipeline AND persists the result to MySQL.
    Returns the same result dict as predict_email(), plus the saved email_id.
    """
    from app import db
    from app.models.db_models import Email, Prediction

    result = predict_email(sender, body)

    # Also compute header flags for the emails table itself
    header_result = analyze_sender(sender)

    email_row = Email(
        sender=sender,
        subject=subject,
        body_snippet=body[:500],  # store a snippet, not the full raw email
        header_mismatch=header_result["header_mismatch"],
    )
    db.session.add(email_row)
    db.session.flush()  # assigns email_row.id without committing yet

    prediction_row = Prediction(
        email_id=email_row.id,
        confidence_score=result["final_score"],
        predicted_label=result["label"],
        top_reasons=result["reasons"],
        model_version="v1-specialist-ensemble",
    )
    db.session.add(prediction_row)
    db.session.commit()

    result["email_id"] = email_row.id
    return result