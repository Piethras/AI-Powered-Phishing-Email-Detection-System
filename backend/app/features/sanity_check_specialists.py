"""
Day 10 - Sanity check both specialist datasets before Week 3 modeling.
Run from backend/: python app\\features\\sanity_check_specialists.py
"""
import pandas as pd

text_df = pd.read_csv("../data/specialist_text.csv")
header_url_df = pd.read_csv("../data/specialist_header_url.csv")

print("=== specialist_text.csv ===")
print("Shape:", text_df.shape)
print("Null counts:")
print(text_df.isnull().sum())
print("Label balance:")
print(text_df["label"].value_counts(normalize=True) * 100)
print("Duplicate text rows:", text_df.duplicated(subset=["text"]).sum())
print()

print("=== specialist_header_url.csv ===")
print("Shape:", header_url_df.shape)
print("Null counts:")
print(header_url_df.isnull().sum())
print("Label balance:")
print(header_url_df["label"].value_counts(normalize=True) * 100)
print("Duplicate sender+body rows:", header_url_df.duplicated(subset=["sender", "body"]).sum())