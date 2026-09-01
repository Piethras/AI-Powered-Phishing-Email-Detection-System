-- =========================================================
-- Phishing Detection System - MySQL Schema (Draft, Day 3)
-- =========================================================
-- Design principle: MySQL's job is ONLY persistence. All decision-making
-- (parsing, scoring) happens in Flask/Python before a row ever gets here.

CREATE DATABASE IF NOT EXISTS phishing_db;
USE phishing_db;

-- Raw + parsed email record
CREATE TABLE IF NOT EXISTS emails (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    sender          VARCHAR(320),
    reply_to        VARCHAR(320),
    subject         TEXT,
    body_snippet    TEXT,              -- first N chars, not full raw storage
    received_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    header_mismatch BOOLEAN DEFAULT FALSE  -- e.g. From vs Received domain mismatch
);

-- One prediction result per email (kept separate from `emails` so we can
-- re-score the same email under a future model version without duplicating it)
CREATE TABLE IF NOT EXISTS predictions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    email_id        INT NOT NULL,
    confidence_score FLOAT NOT NULL,      -- 0.0 - 1.0, phishing likelihood
    predicted_label VARCHAR(20) NOT NULL, -- 'phishing' | 'legitimate'
    top_reasons     JSON,                 -- e.g. ["suspicious_url", "urgency_language"]
    model_version   VARCHAR(50),
    predicted_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_id) REFERENCES emails(id)
);

-- Whitelist: senders/domains the user has explicitly marked as trusted
CREATE TABLE IF NOT EXISTS whitelist (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    sender_domain   VARCHAR(255) NOT NULL UNIQUE,
    added_by        VARCHAR(100),
    added_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Feedback loop: user corrections feed back into future retraining/whitelisting
CREATE TABLE IF NOT EXISTS feedback (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    email_id        INT NOT NULL,
    user_verdict    VARCHAR(20) NOT NULL, -- 'confirmed_phishing' | 'false_positive'
    comment         TEXT,
    submitted_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_id) REFERENCES emails(id)
);
