"""
Day 5 - Run URL heuristics at scale on real data (CEAS_08).
Run from the backend/ folder: python app\features\test_url_checker_real_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from url_checker import analyze_email_urls

df = pd.read_csv("../data/CEAS_08.csv", on_bad_lines="skip")

df["url_analysis"] = df["body"].astype(str).apply(analyze_email_urls)
df["suspicious_url_flag"] = df["url_analysis"].apply(lambda r: r["suspicious_count"] > 0)

legit = df[df["label"] == 0]
phish = df[df["label"] == 1]

legit_rate = legit["suspicious_url_flag"].mean() * 100
phish_rate = phish["suspicious_url_flag"].mean() * 100

print(f"Legitimate (n={len(legit)}): {legit_rate:.2f}% flagged (false positive rate)")
print(f"Phishing   (n={len(phish)}): {phish_rate:.2f}% flagged (true positive rate)")