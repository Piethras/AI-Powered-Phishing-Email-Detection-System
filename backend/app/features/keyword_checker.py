"""
Lightweight multilingual phishing-phrase detector (Day 22).

Not a replacement for the TF-IDF text specialist - that remains
English-only, trained on real labeled data (Day 7). This is a small,
honest, rule-based supplementary signal: does the email contain common
phishing/urgency phrases, in English or French?

This directly addresses a real limitation identified while reasoning
through non-English support: TF-IDF's vocabulary is entirely English
(Day 6-7 training data), so it has near-zero signal on French text.
Header/URL specialists are language-independent and already handle
non-English phishing reasonably (Day 9 architecture). This module closes
part of the remaining text-language gap cheaply, without a full retrain,
which would require a labeled French dataset we do not have.
"""
import re

PHISHING_PHRASES = {
    "en": [
        "verify your account", "account suspended", "click here",
        "confirm your identity", "unusual activity", "update your billing",
        "act now", "your account has been", "immediately to avoid",
    ],
    "fr": [
        "vérifiez votre compte", "compte suspendu", "cliquez ici",
        "confirmez votre identité", "activité inhabituelle",
        "mettez à jour", "agissez maintenant", "votre compte a été",
        "immédiatement pour éviter",
    ],
}


def check_phishing_phrases(text: str) -> dict:
    """Case-insensitive substring match against known phishing phrases."""
    text_lower = (text or "").lower()
    matches = []
    for lang, phrases in PHISHING_PHRASES.items():
        for phrase in phrases:
            if phrase in text_lower:
                matches.append({"phrase": phrase, "language": lang})
    return {
        "match_count": len(matches),
        "matches": matches,
        "languages_detected": sorted(set(m["language"] for m in matches)),
    }


if __name__ == "__main__":
    print("--- English test ---")
    print(check_phishing_phrases("Please verify your account, click here immediately to avoid suspension."))
    print()
    print("--- French test ---")
    print(check_phishing_phrases("Veuillez vérifiez votre compte, cliquez ici immédiatement pour éviter la suspension."))