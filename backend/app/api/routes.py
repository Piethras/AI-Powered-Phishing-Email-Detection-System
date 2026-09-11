"""
API routes - this is the orchestration sequence we reasoned through on Day 3:

1. Raw email arrives at POST /api/predict
2. app.parsers   -> split into headers / body / urls               (Day 4)
3. app.features  -> URL reputation check + NLP feature engineering  (Day 5-9)
4. app.models    -> trained classifier produces a confidence score  (Day 11-15)
5. Result is persisted to MySQL via SQLAlchemy models               (Day 17)
6. JSON response returned -> consumed by the React dashboard        (Day 18)
7. POST /api/feedback -> user corrections stored -> whitelist       (Day 19)
"""
from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health():
    """Sanity check endpoint - confirms the Flask layer is reachable."""
    return jsonify({"status": "ok", "service": "phishing-detection-api"})


@api_bp.route("/predict", methods=["POST"])
def predict():
    """
    Expects: {"sender": "...", "body": "..."}
    Returns: final phishing score, label, and contributing reasons.
    """
    from app.api.pipeline import predict_email

    data = request.json or {}
    sender = data.get("sender", "")
    body = data.get("body", "")

    if not body:
        return jsonify({"error": "'body' is required"}), 400

    result = predict_email(sender, body)
    return jsonify(result)


@api_bp.route("/feedback", methods=["POST"])
def feedback():
    """
    Expects: {"email_id": int, "user_verdict": "safe"|"missed_phishing"}
    Stores feedback and (optionally) updates the whitelist.
    """
    # --- TODO Day 19 ---
    return jsonify({"status": "not_implemented_yet"})