"""
Measures "vocabulary coverage": what fraction of an email's content words
the text specialist's vocabulary recognizes. Read-only, changes nothing.
Run from backend/:  python measure_coverage.py
"""
import re
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app", "features"))

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_features import clean_text

vectorizer = joblib.load("models/text_vectorizer.joblib")
unigrams = {w for w in vectorizer.vocabulary_ if " " not in w}


def coverage(text):
    tokens = re.findall(r"\b\w\w+\b", clean_text(text))
    content = [t for t in tokens if t not in ENGLISH_STOP_WORDS]
    if not content:
        return 0.0, 0
    known = sum(1 for t in content if t in unigrams)
    return known / len(content), len(content)


df = pd.read_csv("../data/specialist_text.csv")
sample = df.sample(3000, random_state=1)
results = [coverage(t) for t in sample["text"].astype(str)]
covs = np.array([r[0] for r in results])
lengths = np.array([r[1] for r in results])

print("English training emails (n=3000), coverage percentiles:")
for p in (1, 5, 10, 25, 50):
    print(f"  {p:>2}th percentile: {np.percentile(covs, p):.2f}")
print(f"  emails with fewer than 5 content words: {(lengths < 5).mean() * 100:.1f}%")

french = {
    "phishing test": "Veuillez vérifiez votre compte, cliquez ici immédiatement pour éviter la suspension.",
    "harmless test": "Bonjour à tous, je vous rappelle que la réunion d'équipe aura lieu lundi à 10h dans la salle de conférence. Merci de préparer vos points d'avancement. Cordialement, Marie",
}
print("\nFrench examples:")
for name, text in french.items():
    c, n = coverage(text)
    print(f"  {name}: coverage {c:.2f} ({n} content words)")