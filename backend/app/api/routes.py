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
    from app.api.pipeline import predict_and_save

    data = request.json or {}
    sender = data.get("sender", "")
    body = data.get("body", "")

    if not body:
        return jsonify({"error": "'body' is required"}), 400

    result = predict_and_save(sender, body, data.get("subject", ""))
    return jsonify(result)

@api_bp.route("/predictions", methods=["GET"])
def get_predictions():
    """
    Returns recent predictions with their linked email info, newest first.
    Powers the Confidence Score Dashboard (Day 3 requirement).
    """
    from app.models.db_models import Email, Prediction

    results = (
        Prediction.query
        .join(Email, Prediction.email_id == Email.id)
        .order_by(Prediction.predicted_at.desc())
        .limit(50)
        .all()
    )

    return jsonify([
        {
            "email_id": p.email_id,
            "sender": p.email.sender,
            "subject": p.email.subject,
            "body_snippet": p.email.body_snippet,
            "confidence_score": p.confidence_score,
            "predicted_label": p.predicted_label,
            "reasons": p.top_reasons,
            "predicted_at": p.predicted_at.isoformat(),
        }
        for p in results
    ])

@api_bp.route("/predictions/all", methods=["GET"])
def get_all_predictions():
    """
    Returns ALL predictions (no limit), for the Email History page.
    Supports optional query params: ?label=phishing|legitimate
    """
    from app.models.db_models import Email, Prediction

    query = Prediction.query.join(Email, Prediction.email_id == Email.id)

    label_filter = request.args.get("label")
    if label_filter == "phishing":
        query = query.filter(Prediction.predicted_label == "phishing")
    elif label_filter == "legitimate":
        query = query.filter(Prediction.predicted_label == "legitimate")
    elif label_filter == "uncertain":
        query = query.filter(Prediction.predicted_label == "uncertain")

    results = query.order_by(Prediction.predicted_at.desc()).all()

    return jsonify([
        {
            "email_id": p.email_id,
            "sender": p.email.sender,
            "subject": p.email.subject,
            "body_snippet": p.email.body_snippet,
            "confidence_score": p.confidence_score,
            "predicted_label": p.predicted_label,
            "reasons": p.top_reasons,
            "predicted_at": p.predicted_at.isoformat(),
        }
        for p in results
    ])

@api_bp.route("/insights", methods=["GET"])
def get_insights():
    """
    Aggregates stored predictions: totals, top flagged domains, and a
    daily breakdown for the dashboard chart. Handles the third
    "uncertain" label (low text coverage, needs review).
    """
    from app.models.db_models import Email, Prediction
    from collections import Counter, defaultdict
    import re

    all_predictions = (
        Prediction.query.join(Email, Prediction.email_id == Email.id).all()
    )

    domain_counter = Counter()
    daily_counts = defaultdict(lambda: {"phishing": 0, "legitimate": 0, "uncertain": 0})

    for p in all_predictions:
        day = p.predicted_at.strftime("%Y-%m-%d")
        daily_counts[day][p.predicted_label] += 1

        if p.predicted_label == "phishing":
            sender = p.email.sender or ""
            match = re.search(r"@([\w.-]+)", sender)
            if match:
                domain_counter[match.group(1).lower()] += 1

    daily_series = [
        {"date": day, **counts}
        for day, counts in sorted(daily_counts.items())
    ]

    total = len(all_predictions)
    total_flagged = sum(1 for p in all_predictions if p.predicted_label == "phishing")
    total_uncertain = sum(1 for p in all_predictions if p.predicted_label == "uncertain")

    return jsonify({
        "total_scanned": total,
        "total_flagged": total_flagged,
        "total_uncertain": total_uncertain,
        "total_legitimate": total - total_flagged - total_uncertain,
        "flagged_rate": round(total_flagged / total, 4) if total > 0 else 0,
        "top_flagged_domains": [{"domain": d, "count": c} for d, c in domain_counter.most_common(10)],
        "daily_series": daily_series,
    })
@api_bp.route("/system-info", methods=["GET"])
def system_info():
    """Returns real system configuration for the Settings page."""
    from app.models.db_models import Email, Whitelist

    return jsonify({
        "model_version": "v1-specialist-ensemble",
        "threshold": 0.70,
        "specialists": ["text (TF-IDF + Random Forest)", "header", "url"],
        "total_emails_in_db": Email.query.count(),
        "whitelisted_domains": Whitelist.query.count(),
        "database": "MySQL (phishing_db)",
    })

@api_bp.route("/upload", methods=["POST"])
def upload_email():
    """
    Accepts a raw .eml file (multipart/form-data, field name 'file') OR
    raw email text sent as a Blob under the same field name.
    Parses it with parse_raw_email() (Day 4) and scores it live.
    """
    from app.parsers.header_parser import parse_raw_email
    from app.api.pipeline import predict_and_save

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Send as multipart/form-data with key 'file'."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    raw_bytes = file.read()
    try:
        raw_text = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        raw_text = raw_bytes.decode("latin-1", errors="replace")

    parsed = parse_raw_email(raw_text)
    sender = parsed["from"]
    subject = parsed["subject"]
    body = parsed["body"]

    if not body:
        return jsonify({"error": "Could not extract body text from this file. Is it a valid .eml file?"}), 400

    result = predict_and_save(sender, body, subject)
    return jsonify(result)


@api_bp.route("/feedback", methods=["POST"])
@api_bp.route("/feedback", methods=["POST"])
def feedback():
    """
    Expects: {"email_id": int, "user_verdict": "confirmed_phishing"|"false_positive", "comment": "..."}
    Stores feedback with an audit trail (Day 3 safeguard: never auto-alters
    classifier behavior from a single submission - just recorded for review).
    """
    from app import db
    from app.models.db_models import Feedback

    data = request.json or {}
    email_id = data.get("email_id")
    verdict = data.get("user_verdict")

    valid_verdicts = ("true_positive", "false_positive", "true_negative", "false_negative")
    if not email_id or verdict not in valid_verdicts:
        return jsonify({"error": "email_id and a valid user_verdict are required"}), 400

    entry = Feedback(
        email_id=email_id,
        user_verdict=verdict,
        comment=data.get("comment", ""),
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({"status": "recorded", "feedback_id": entry.id})

@api_bp.route("/feedback/all", methods=["GET"])
def get_all_feedback():
    """Returns all submitted feedback, joined with the related email, for human review (Day 3 design principle)."""
    from app.models.db_models import Email, Feedback

    results = (
        Feedback.query
        .join(Email, Feedback.email_id == Email.id)
        .order_by(Feedback.submitted_at.desc())
        .all()
    )

    return jsonify([
        {
            "feedback_id": f.id,
            "email_id": f.email_id,
            "sender": f.email.sender,
            "subject": f.email.subject,
            "user_verdict": f.user_verdict,
            "comment": f.comment,
            "submitted_at": f.submitted_at.isoformat(),
        }
        for f in results
    ])

@api_bp.route("/whitelist", methods=["GET"])
def get_whitelist():
    """Returns all whitelisted sender domains."""
    from app.models.db_models import Whitelist

    entries = Whitelist.query.order_by(Whitelist.added_at.desc()).all()
    return jsonify([
        {"id": w.id, "sender_domain": w.sender_domain, "added_by": w.added_by, "added_at": w.added_at.isoformat()}
        for w in entries
    ])


@api_bp.route("/whitelist", methods=["POST"])
def add_whitelist():
    """
    Expects: {"sender_domain": "example.com", "added_by": "Nyanga"}
    This is a DELIBERATE action, distinct from /api/feedback - Day 3's
    safeguard against feedback poisoning: whitelisting a domain requires
    an explicit, separate action, not a side-effect of casual feedback.
    """
    from app import db
    from app.models.db_models import Whitelist

    data = request.json or {}
    domain = (data.get("sender_domain") or "").strip().lower()
    added_by = data.get("added_by", "unknown")

    if not domain:
        return jsonify({"error": "sender_domain is required"}), 400

    existing = Whitelist.query.filter_by(sender_domain=domain).first()
    if existing:
        return jsonify({"error": f"{domain} is already whitelisted"}), 400

    entry = Whitelist(sender_domain=domain, added_by=added_by)
    db.session.add(entry)
    db.session.commit()

    return jsonify({"status": "added", "id": entry.id, "sender_domain": domain})

@api_bp.route("/emails/<int:email_id>", methods=["DELETE"])
def delete_email(email_id):
    """
    Deletes a stored email and its associated predictions/feedback.
    Answers the 'is data discarded' question with a real mechanism,
    not just a policy statement.
    """
    from app import db
    from app.models.db_models import Email, Prediction, Feedback

    email = Email.query.get(email_id)
    if not email:
        return jsonify({"error": "not found"}), 404

    Prediction.query.filter_by(email_id=email_id).delete()
    Feedback.query.filter_by(email_id=email_id).delete()
    db.session.delete(email)
    db.session.commit()
    return jsonify({"status": "deleted", "email_id": email_id})