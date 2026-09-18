# Day 14 — Error Analysis

## Errors at threshold=0.70 (test set, n=14,946)
- False positives (legit called phishing): 58 (0.78% of legitimate)
- False negatives (phishing called legit): 553 (7.37% of phishing)

## Pattern 1: False positives cluster on very short/sparse emails
Examples: "unsubscribe Unsubscribe", automated delivery-failure notices,
short mailing-list forwards with a single URL, brief internal shorthand.

**Root cause:** TF-IDF relies on having enough words to build a reliable
signal. Very short emails (a handful of words) give the model little
evidence to work with - if those few words happen to overlap with
phishing-associated vocabulary or score high on rarity, there's not
enough other content to balance that signal out. This is a structural
limitation of word-frequency-based methods on sparse text, not a bug.

## Pattern 2: False negatives cluster on garbled/obfuscated text
Examples: encoded/foreign-character spam, deliberate word-salad
(nonsense words strung together), scrambled text designed to evade
keyword-based filters.

**Root cause:** this content is intentionally constructed to defeat
content-analysis approaches. This is NOT unique to TF-IDF - even
contextual models like BERT (Day 8) would struggle, since they also
rely on recognizing real words and their relationships. This is closer
to a fundamental limit of text-based detection generally, not a
specific weakness of our chosen method.

## Why this doesn't undermine the system design
Both patterns are mitigated by Day 9's defense-in-depth architecture:
an email using obfuscated text to evade the NLP module may still be
caught by header analysis (Day 4) or URL reputation checks (Day 5),
which don't depend on the body text being meaningful at all. No single
module is expected to catch everything - this is the explicit design
rationale, now supported by concrete evidence of where the text module
specifically struggles.

## Honest limitation for the report
This system is less reliable on very short emails and on deliberately
obfuscated/garbled text, regardless of modeling approach chosen. Future
work could add a minimum-length confidence adjustment, or weight header/
URL signals more heavily when body text is too sparse or garbled to
trust.