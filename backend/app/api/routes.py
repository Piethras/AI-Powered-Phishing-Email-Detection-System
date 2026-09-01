"""
API routes - this is the orchestration sequence we reasoned through on Day 3:

1. Raw email arrives at POST /api/predict
2. app.parsers   -> split into headers / body / urls               (Day 4)
3. app.features  -> URL reputation check + NLP feature engineering  (Day 5-9)
4. app.models    -> trained classifier produces a confidence score  (Day 11-15)
5. Result is persisted to MySQL via SQLAlchemy models               (Day 17)
6. JSON response returned -> consumed by the React dashboard        (Day 18)
7. POST /api/feedback -> user corrections stored -> whitelist       (Day 19)

Each numbered step is currently a placeholder (TODO) and will be filled in
as we reach that day in the project plan. The skeleton exists now so the
overall data flow is fixed and testable end-to-end from day one.
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
    Expects: raw email content (JSON: {"raw_email": "..."})
    Returns: {"score": float, "label": "phishing"|"legitimate", "reasons": [...]}
    """
    raw_email = request.json.get("raw_email", "")

    # --- TODO Day 4: parse headers/body/urls from raw_email ---
    # parsed = parse_email(raw_email)

    # --- TODO Day 5-9: compute header/url/text features ---
    # features = build_features(parsed)

    # --- TODO Day 11-15: run trained classifier ---
    # score, reasons = classifier.predict(features)

    # --- TODO Day 17: persist result to MySQL ---
    # save_prediction(parsed, score, reasons)

    # Placeholder response so the endpoint is testable end-to-end now
    return jsonify({
        "score": None,
        "label": "not_implemented_yet",
        "reasons": [],
        "note": "Pipeline skeleton only - modules wired in on their scheduled days."
    })


@api_bp.route("/feedback", methods=["POST"])
def feedback():
    """
    Expects: {"email_id": int, "user_verdict": "safe"|"missed_phishing"}
    Stores feedback and (optionally) updates the whitelist.
    """
    # --- TODO Day 19 ---
    return jsonify({"status": "not_implemented_yet"})
