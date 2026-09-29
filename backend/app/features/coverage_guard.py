import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_features import clean_text


def text_coverage(text, known_unigrams):
    """Fraction of an email's content words that the text model's vocabulary recognizes."""
    tokens = re.findall(r"\b\w\w+\b", clean_text(text))
    content = [t for t in tokens if t not in ENGLISH_STOP_WORDS]
    if not content:
        return 0.0
    return sum(1 for t in content if t in known_unigrams) / len(content)