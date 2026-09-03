"""
NLP Feature Engineering - TF-IDF (Day 7)

Builds on the hand-calculated TF-IDF concept from Day 6. scikit-learn's
TfidfVectorizer does the same TF x IDF math we derived by hand, but across
the entire vocabulary of thousands of emails at once.

We use `phishing_email.csv` (the combined dataset) since it has both
classes in a consistent text-only format (subject/body combined as
`text_combined`), avoiding the source-correlated leakage risk identified
on Day 2.
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Basic cleaning - TfidfVectorizer can do some of this itself, but being
# explicit here makes the preprocessing step visible and defensible,
# rather than hidden inside library defaults.
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', ' URL ', text)   # normalize URLs to a single token
    text = re.sub(r'[^a-z\s]', ' ', text)      # strip punctuation/numbers
    text = re.sub(r'\s+', ' ', text).strip()   # collapse whitespace
    return text


def build_tfidf_features(texts, max_features=3000):
    """
    Fits a TF-IDF vectorizer on a list/Series of email texts.
    Returns the fitted vectorizer and the resulting feature matrix.
    """
    cleaned = [clean_text(t) for t in texts]
    vectorizer = TfidfVectorizer(
        max_features=max_features,   # cap vocabulary size - keeps this manageable
        stop_words="english",        # removes "the", "to", "is", etc. (Day 6 concept)
        ngram_range=(1, 2),          # single words AND two-word phrases (Day 8 upgrade)
    )
    matrix = vectorizer.fit_transform(cleaned)
    return vectorizer, matrix


def top_terms_by_class(vectorizer, matrix, labels, label_value, top_n=20):
    """
    Given a fitted vectorizer + matrix + labels, find the words with the
    highest AVERAGE TF-IDF score within one class (phishing or legit).
    This is our Day 7 sanity check: do the top words make sense?
    """
    import numpy as np
    feature_names = vectorizer.get_feature_names_out()
    mask = (labels == label_value)
    class_matrix = matrix[mask.values if hasattr(mask, "values") else mask]
    avg_scores = class_matrix.mean(axis=0).A1  # convert sparse matrix row to array
    top_indices = avg_scores.argsort()[::-1][:top_n]
    return [(feature_names[i], round(avg_scores[i], 4)) for i in top_indices]


if __name__ == "__main__":
    # Quick sanity test using our Day 1/6 toy sentences
    toy_sentences = [
        "click here to verify your account",
        "click here to see photos from the party",
        "your account statement is ready to view",
    ]
    vec, mat = build_tfidf_features(toy_sentences, max_features=50)
    print("Vocabulary:", vec.get_feature_names_out())
    print("Matrix shape:", mat.shape)
    print("Row 0 (verify sentence) as dense array:")
    print(mat[0].toarray())