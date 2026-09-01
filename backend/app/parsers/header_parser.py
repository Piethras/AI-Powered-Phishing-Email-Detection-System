"""
Header & Sender Analysis (Day 4)

Two-part design, matching the two real-world input formats we'll encounter:

1. parse_raw_email() - for genuine raw .eml/MIME text (production input).
   Uses Python's built-in `email` package rather than hand-rolled string
   splitting, because raw email headers can be folded across lines,
   encoded (e.g. =?UTF-8?B?...?=), and repeated (multiple Received: lines).
   Hand-rolled parsing would silently mishandle these RFC 5322/MIME cases.

2. analyze_sender() - for the "Display Name <address>" format our labeled
   training data (CEAS_08, SpamAssassin) already provides in a single
   `sender` column. This is the format we can actually test our spoofing
   heuristics against today.

Known limitation (documented, not hidden): our labeled datasets provide
sender/receiver/date but not the full Received: header chain discussed
on Day 1. Full received-chain verification is only possible once real
raw .eml files are used as input (production scenario). Sender-address
analysis below is what our current dataset can support.
"""
import re
from email import policy
from email.parser import BytesParser, Parser
from email.utils import parseaddr

# A small reference list of commonly-impersonated brands for demo purposes.
# In a production system this would be a longer, maintained list.
COMMON_IMPERSONATED_BRANDS = {
    "paypal": ["paypal.com"],
    "amazon": ["amazon.com"],
    "apple": ["apple.com"],
    "microsoft": ["microsoft.com", "live.com", "outlook.com"],
    "bank of america": ["bankofamerica.com"],
    "netflix": ["netflix.com"],
    "google": ["google.com", "gmail.com"],
}

FREE_WEBMAIL_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com"}


def parse_raw_email(raw_bytes_or_str):
    """
    Parse a genuine raw .eml message using Python's email package.
    Returns a dict with headers-of-interest and decoded body text.
    This is the path a real deployed system uses on incoming mail.
    """
    if isinstance(raw_bytes_or_str, bytes):
        msg = BytesParser(policy=policy.default).parsebytes(raw_bytes_or_str)
    else:
        msg = Parser(policy=policy.default).parsestr(raw_bytes_or_str)

    # get_all() is essential here - a message can have MULTIPLE Received
    # headers (the chain from Day 1), and a naive .get() would only return
    # the first/last one depending on implementation, losing the chain.
    received_chain = msg.get_all("Received", [])

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
                break
    else:
        body = msg.get_content()

    return {
        "from": msg.get("From", ""),
        "reply_to": msg.get("Reply-To", ""),
        "return_path": msg.get("Return-Path", ""),
        "received_chain": [str(r) for r in received_chain],
        "subject": msg.get("Subject", ""),
        "body": body,
    }


def analyze_sender(sender_field: str) -> dict:
    """
    Analyze a "Display Name <address>" sender field for spoofing signals.
    This is what we can test today against CEAS_08 / SpamAssassin.
    """
    display_name, address = parseaddr(sender_field or "")
    domain = address.split("@")[-1].lower() if "@" in address else ""
    display_lower = (display_name or "").lower()

    flags = []

    # Check 1: display name mentions a known brand, domain doesn't match it
    for brand, valid_domains in COMMON_IMPERSONATED_BRANDS.items():
        if brand in display_lower and domain not in valid_domains:
            flags.append(f"brand_mismatch:{brand}_but_domain_is_{domain}")

    # Check 2: free webmail domain used while display name suggests an org
    org_signal_words = ["support", "security", "team", "service", "official", "admin", "bank"]
    if domain in FREE_WEBMAIL_DOMAINS and any(w in display_lower for w in org_signal_words):
        flags.append(f"org_claim_on_free_webmail:{domain}")

    # Check 3: simple homoglyph/lookalike heuristic - digit substitutions
    # common in lookalike domains (0 for o, 1 for l, etc.)
    if re.search(r"[0-9]", domain.split(".")[0]) and any(
        brand in display_lower for brand in COMMON_IMPERSONATED_BRANDS
    ):
        flags.append(f"possible_lookalike_domain:{domain}")

    return {
        "display_name": display_name,
        "address": address,
        "domain": domain,
        "flags": flags,
        "header_mismatch": len(flags) > 0,
    }


if __name__ == "__main__":
    # Quick manual sanity tests before running on the real dataset
    tests = [
        '"PayPal Support" <security@paypa1-secure.ru>',
        '"Bank of America Security" <alerts@gmail.com>',
        "Young Esposito <Young@iworld.de>",
        "Guido van Rossum <guido@python.org>",
    ]
    for t in tests:
        print(t, "->", analyze_sender(t))
