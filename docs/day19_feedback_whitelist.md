
## Bug found and fixed: feedback verdict mislabeling on legitimate-labeled rows

**Discovered by asking a simple clarifying question**: "what does clicking
thumbs-down mean?" revealed the feedback schema only supported two verdict
values (`confirmed_phishing`, `false_positive`), forced onto four real
outcomes. This correctly handled phishing-labeled rows but silently
mislabeled BOTH outcomes on legitimate-labeled rows:
- Thumbs-up on a correct "Legitimate" call incorrectly stored
  `false_positive` (should mean "correctly legitimate", not "wrongly
  flagged as phishing" - the opposite of what was recorded).
- Thumbs-down on a missed phishing email incorrectly stored
  `confirmed_phishing` rather than being distinguished as a false negative.

**Fix:** expanded verdict values to the standard confusion-matrix terms
from Day 1 (true_positive, false_positive, true_negative, false_negative),
updated schema.sql, backend validation, and the button click handlers to
select the correct term based on BOTH the row's predicted label AND
which button was clicked.

**Verified with real evidence:** the same email (id 5), thumbs-up clicked
twice - once before the fix (incorrectly stored `false_positive`) and
once after (correctly stored `true_negative`) - both visible side-by-side
in the feedback table, providing direct before/after proof the fix works.

**Lesson:** a schema designed with only 2 verdict categories couldn't
represent all 4 real confusion-matrix outcomes. Worth remembering when
designing data models: enumerate the actual state space (here, 2 possible
labels x 2 possible user judgments = 4 outcomes) rather than assuming a
binary "agree/disagree" is sufficient.