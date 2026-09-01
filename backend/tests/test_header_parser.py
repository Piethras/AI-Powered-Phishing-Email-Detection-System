"""
Tests for app.parsers.header_parser (Day 4 deliverable)

Run with: python3 -m pytest backend/tests/test_header_parser.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import importlib.util

spec = importlib.util.spec_from_file_location(
    "header_parser",
    os.path.join(os.path.dirname(__file__), "..", "app", "parsers", "header_parser.py"),
)
header_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(header_parser)

analyze_sender = header_parser.analyze_sender
parse_raw_email = header_parser.parse_raw_email


# ---------- analyze_sender() tests ----------

def test_detects_brand_domain_mismatch():
    result = analyze_sender('"PayPal Support" <security@paypa1-secure.ru>')
    assert result["header_mismatch"] is True
    assert any("brand_mismatch" in f for f in result["flags"])


def test_detects_org_claim_on_free_webmail():
    result = analyze_sender('"Bank of America Security" <alerts@gmail.com>')
    assert result["header_mismatch"] is True
    assert any("org_claim_on_free_webmail" in f for f in result["flags"])


def test_clean_sender_produces_no_flags():
    result = analyze_sender("Guido van Rossum <guido@python.org>")
    assert result["header_mismatch"] is False
    assert result["flags"] == []


def test_generic_spam_sender_not_falsely_flagged_as_brand_impersonation():
    # Documents the Day 4 finding: senders with no brand claim correctly
    # produce no flags, even if they are (per dataset label) phishing/spam.
    # This is intentional - this check targets brand impersonation
    # specifically, not phishing in general.
    result = analyze_sender("Daily Top 10 <drapent1986@capespan.be>")
    assert result["flags"] == []


def test_handles_malformed_or_empty_sender_gracefully():
    result = analyze_sender("keaten <>")
    assert result["address"] == ""
    assert result["domain"] == ""
    # should not crash, and should not falsely flag
    assert isinstance(result["flags"], list)


# ---------- parse_raw_email() tests ----------

RAW_EMAIL_WITH_FOLDED_HEADER_AND_CHAIN = """From: "PayPal Support" <security@paypa1-secure.ru>
Reply-To: refunds@totally-legit-paypal.ru
Return-Path: <bounce@paypa1-secure.ru>
Received: from mail.victimcompany.com by mx.victimcompany.com; Tue, 05 Aug 2008 16:31:00 -0700
Received: from relay.suspicious-host.ru by mail.victimcompany.com; Tue, 05 Aug 2008 16:30:55 -0700
Received: from [192.168.1.5] by relay.suspicious-host.ru; Tue, 05 Aug 2008 16:30:40 -0700
Subject: Your account has been suspended, please verify your
 identity immediately to avoid permanent loss of access
Content-Type: text/plain

Dear customer, click here to verify: http://paypa1-secure.ru/verify
"""


def test_folded_header_reassembled_correctly():
    """A naive line-by-line parser would truncate this subject mid-sentence."""
    result = parse_raw_email(RAW_EMAIL_WITH_FOLDED_HEADER_AND_CHAIN)
    assert "identity immediately to avoid permanent loss of access" in result["subject"]
    assert result["subject"].count("\n") == 0  # fully reassembled into one line


def test_multiple_received_headers_all_captured():
    """A naive .get('Received') would only return one of these three."""
    result = parse_raw_email(RAW_EMAIL_WITH_FOLDED_HEADER_AND_CHAIN)
    assert len(result["received_chain"]) == 3
    assert "suspicious-host.ru" in result["received_chain"][1]


def test_body_extracted():
    result = parse_raw_email(RAW_EMAIL_WITH_FOLDED_HEADER_AND_CHAIN)
    assert "verify" in result["body"].lower()


if __name__ == "__main__":
    # Allow running without pytest installed, as a plain script
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {t.__name__} -> {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
