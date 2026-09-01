"""
Day 5 debugging - inspect WHICH legitimate emails are triggering our
URL heuristics, and WHY, before drawing conclusions.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from url_checker import analyze_email_urls

df = pd.read_csv("../data/CEAS_08.csv", on_bad_lines="skip")
df["url_analysis"] = df["body"].astype(str).apply(analyze_email_urls)
df["suspicious_url_flag"] = df["url_analysis"].apply(lambda r: r["suspicious_count"] > 0)

flagged_legit = df[(df["label"] == 0) & (df["suspicious_url_flag"])]

print(f"Total flagged legitimate emails: {len(flagged_legit)}")
print()

for i, row in flagged_legit.head(10).iterrows():
    print("SENDER:", row["sender"])
    for detail in row["url_analysis"]["details"]:
        if detail["suspicious"]:
            print("  Flagged URL:", detail["url"], "-> reasons:", detail["flags"])
    print("---")