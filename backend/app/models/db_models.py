"""
SQLAlchemy models matching backend/data/schema.sql (Day 3/17).
These let Flask read/write to MySQL using Python objects instead of raw SQL.
"""
from app import db
from datetime import datetime


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(320))
    reply_to = db.Column(db.String(320))
    subject = db.Column(db.Text)
    body_snippet = db.Column(db.Text)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    header_mismatch = db.Column(db.Boolean, default=False)

    predictions = db.relationship("Prediction", backref="email", lazy=True)


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    predicted_label = db.Column(db.String(20), nullable=False)
    top_reasons = db.Column(db.JSON)
    model_version = db.Column(db.String(50))
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)


class Whitelist(db.Model):
    __tablename__ = "whitelist"

    id = db.Column(db.Integer, primary_key=True)
    sender_domain = db.Column(db.String(255), unique=True, nullable=False)
    added_by = db.Column(db.String(100))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False)
    user_verdict = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)