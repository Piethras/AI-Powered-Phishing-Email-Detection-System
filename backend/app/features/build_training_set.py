"""
Day 7 - Build our own combined training set with KNOWN, transparent
source composition, rather than relying on the opaque phishing_email.csv.

Legitimate: Enron + CEAS_08 legit + SpamAssassin legit
Phishing:   CEAS_08 phishing + SpamAssassin phishing
(Nazario excluded from training - single-class source, Day 2 finding)

Output: data/training_set.csv with columns [text, label, source]
The `source` column is kept so we can always audit composition later -
exactly the transparency our previous approach was missing.
"""
import pandas as pd

enron = pd.read_csv("../data/Enron.csv", on_bad_lines="skip")
ceas = pd.read_csv("../data/CEAS_08.csv", on_bad_lines="skip")
spamassassin = pd.read_csv("../data/SpamAssasin.csv", on_bad_lines="skip")

def make_rows(df, text_cols, label_col, source_name, label_filter=None):
    d = df.copy()
    if label_filter is not None:
        d = d[d[label_col] == label_filter]
    text = d[text_cols[0]].astype(str)
    for col in text_cols[1:]:
        text = text + " " + d[col].astype(str)
    return pd.DataFrame({
        "text": text,
        "label": d[label_col].values,
        "source": source_name,
    })

parts = [
    make_rows(enron, ["subject", "body"], "label", "enron"),  # both classes, kept as-is
    make_rows(ceas, ["subject", "body"], "label", "ceas08"),
    make_rows(spamassassin, ["subject", "body"], "label", "spamassassin"),
]

training_set = pd.concat(parts, ignore_index=True)
training_set = training_set.dropna(subset=["text", "label"])

print("=== Final training set composition ===")
print(f"Total rows: {len(training_set)}")
print()
print("By source and label:")
print(training_set.groupby(["source", "label"]).size())
print()
print("Overall label balance:")
print(training_set["label"].value_counts(normalize=True) * 100)

training_set.to_csv("../data/training_set.csv", index=False)
print("\nSaved to data/training_set.csv")