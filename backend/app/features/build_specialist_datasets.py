"""
Day 9 - Build separate training datasets for each specialist model,
respecting which sources actually support which feature type.

Text specialist:   ALL sources (every source has subject/body)
Header specialist: CEAS_08 + SpamAssassin only (Enron lacks sender field)
URL specialist:    CEAS_08 + SpamAssassin only (Enron lacks urls field)
"""
import pandas as pd

# Text dataset - reuse what Day 7 already built
text_df = pd.read_csv("../data/training_set.csv")
print(f"Text specialist dataset: {len(text_df)} rows (all sources)")
text_df.to_csv("../data/specialist_text.csv", index=False)

# Header + URL dataset - only sources with sender/urls fields
ceas = pd.read_csv("../data/CEAS_08.csv", on_bad_lines="skip")
spamassassin = pd.read_csv("../data/SpamAssasin.csv", on_bad_lines="skip")

header_url_df = pd.concat([
    ceas[["sender", "body", "urls", "label"]].assign(source="ceas08"),
    spamassassin[["sender", "body", "urls", "label"]].assign(source="spamassassin"),
], ignore_index=True).dropna(subset=["sender", "label"])

print(f"Header/URL specialist dataset: {len(header_url_df)} rows (CEAS_08 + SpamAssassin only)")
print(header_url_df.groupby(["source", "label"]).size())

header_url_df.to_csv("../data/specialist_header_url.csv", index=False)

print("\nSaved: data/specialist_text.csv, data/specialist_header_url.csv")
