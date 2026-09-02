"""
Day 7 - Inspect top TF-IDF terms per class on the real dataset.
Run from backend/: python app\\features\\inspect_top_terms.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from text_features import build_tfidf_features, top_terms_by_class

df = pd.read_csv("../data/training_set.csv", on_bad_lines="skip")
print(f"Loaded {len(df)} rows")
print(df.columns.tolist())

vectorizer, matrix = build_tfidf_features(df["text"], max_features=3000)

print("\n=== Top 20 terms - LEGITIMATE (label=0) ===")
for word, score in top_terms_by_class(vectorizer, matrix, df["label"], 0):
    print(f"  {word:20s} {score}")

print("\n=== Top 20 terms - PHISHING (label=1) ===")
for word, score in top_terms_by_class(vectorizer, matrix, df["label"], 1):
    print(f"  {word:20s} {score}")