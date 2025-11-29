import json
import os
import itertools
import unicodedata
from typing import Dict, List


class WordDistanceAnalyzer:

    def __init__(self, data_path: str, output_path: str):
        self.data_path = data_path
        self.output_path = output_path
        self.translated_data = None
        self.word_distances = None

    @staticmethod
    def normalize(word: str) -> str:
        if not isinstance(word, str):
            return word

        nfkd = unicodedata.normalize("NFD", word)
        no_diacritics = "".join(ch for ch in nfkd if not unicodedata.combining(ch))

        return no_diacritics.lower()

    @staticmethod
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
                    dp[i - 1][j] + 1,        # deletion
                    dp[i][j - 1] + 1,        # insertion
                    dp[i - 1][j - 1] + cost  # substitution
                )

        return dp[-1][-1]

    def load_translations(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.translated_data = json.load(f)

    def compute_distances(self) -> List[Dict]:
        results = []

        for topic_entry in self.translated_data:
            topic = topic_entry["topic"].lower()
            words = topic_entry["words"]

            languages = [lang for lang in words[0].keys() if lang != "topic"]

            for word_entry in words:
                for lang_a, lang_b in itertools.combinations(languages, 2):
                    w1_original = word_entry.get(lang_a, "")
                    w2_original = word_entry.get(lang_b, "")

                    w1 = self.normalize(w1_original)
                    w2 = self.normalize(w2_original)

                    if not w1 or not w2:
                        continue

                    raw_dist = self.levenshtein(w1, w2)

                    max_len = max(len(w1), len(w2))
                    normalized_dist = raw_dist / max_len if max_len > 0 else 0

                    results.append({
                        "topic": topic,
                        "language_pair": f"{lang_a}-{lang_b}",
                        "word_pair": [w1_original, w2_original],
                        "distance": round(normalized_dist, 4)
                    })

        self.word_distances = results
        return results

    def save_results(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.word_distances, f, indent=2, ensure_ascii=False)

    def run(self):
        self.load_translations()
        self.compute_distances()
        self.save_results()

        print(f"\n✓ Word distance analysis completed!")
        print(f"  Output: {self.output_path}")
        print(f"  Total word pairs analyzed: {len(self.word_distances)}")


def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    data_path = os.path.join(base_path, "data/translated.json")
    output_path = os.path.join(base_path, "data/analysis/word_distance.json")

    analyzer = WordDistanceAnalyzer(data_path, output_path)
    analyzer.run()


if __name__ == "__main__":
    main()