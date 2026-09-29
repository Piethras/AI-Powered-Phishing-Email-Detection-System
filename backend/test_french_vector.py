import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app", "features"))
import joblib
from text_features import clean_text

vectorizer = joblib.load("models/text_vectorizer.joblib")

french_text = "Veuillez vérifiez votre compte, cliquez ici immédiatement pour éviter la suspension."
cleaned = clean_text(french_text)
print("Cleaned text:", repr(cleaned))

vec = vectorizer.transform([cleaned])
print("Non-zero features found:", vec.nnz)
print("Total vocabulary size:", vec.shape[1])

# Show which words (if any) actually matched something in the vocabulary
feature_names = vectorizer.get_feature_names_out()
nonzero_indices = vec.nonzero()[1]
matched_words = [feature_names[i] for i in nonzero_indices]
print("Matched vocabulary words:", matched_words)