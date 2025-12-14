import unicodedata
import json
import os
from typing import List, Dict

def normalize(word: str) -> str:
    if not isinstance(word, str):
        return word

    nfkd = unicodedata.normalize("NFD", word)
    no_diacritics = "".join(ch for ch in nfkd if not unicodedata.combining(ch))

    return no_diacritics.lower()

def levenshtein(a: str, b: str) -> int:
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
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[-1][-1]

def load_translations(data_path: str) -> List[Dict]:
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for topic_entry in data:
        for word_entry in topic_entry["words"]:
            for lang, word in word_entry.items():
                word_entry[lang] = normalize(word)
    return data

def get_translations_path(base_path: str) -> str:
    return os.path.join(base_path, "data", "translated.json")
