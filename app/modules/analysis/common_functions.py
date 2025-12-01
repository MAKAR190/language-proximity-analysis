import unicodedata
import json
import os
from typing import List, Dict


# ---------------------------------------------------------
# Normalize words: remove diacritics and lowercase
# ---------------------------------------------------------
def normalize(word: str) -> str:
    """
    Remove diacritics and convert to lowercase.
    Example:
      'Liście'  → 'liscie'
      'légume'  → 'legume'
      'feuilles' stays the same
    """
    if not isinstance(word, str):
        return word

    # Unicode decomposition:  "ć" → "c" + accent
    nfkd = unicodedata.normalize("NFD", word)

    # Remove all diacritic marks
    no_diacritics = "".join(ch for ch in nfkd if not unicodedata.combining(ch))

    return no_diacritics.lower()


# ---------------------------------------------------------
# Levenshtein distance (Wagner-Fischer algorithm)
# ---------------------------------------------------------
def levenshtein(a: str, b: str) -> int:
    """
    Compute Levenshtein distance between two strings.
    """
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)

    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )

    return dp[-1][-1]


# ---------------------------------------------------------
# Load translations from JSON and normalize words
# ---------------------------------------------------------
def load_translations(data_path: str) -> List[Dict]:
    """Load translated topics/words from JSON and normalize all words."""
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for topic_entry in data:
        for word_entry in topic_entry["words"]:
            for lang, word in word_entry.items():
                word_entry[lang] = normalize(word)

    return data

# ---------------------------------------------------------
# Helper to get full path to translated.json
# ---------------------------------------------------------
def get_translations_path(base_path: str) -> str:
    """
    Return the full path to the translations JSON file.
    """
    return os.path.join(base_path, "data", "translated.json")
