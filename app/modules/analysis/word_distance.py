# word_distance_analyzer.py
import json
import os
import itertools
from typing import List, Dict
from common_functions import levenshtein, load_translations


class WordDistanceAnalyzer:
    def __init__(self, data_path: str, output_path: str):
        self.data_path = data_path
        self.output_path = output_path
        self.translated_data = None
        self.word_distances: List[Dict] = []

    def load_and_normalize_translations(self) -> None:
        self.translated_data = load_translations(self.data_path)
        print(f"Loaded and normalized {sum(len(t['words']) for t in self.translated_data)} words across topics.")

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

                    w1 = word_entry.get(lang_a, "")
                    w2 = word_entry.get(lang_b, "")

                    if not w1 or not w2:
                        continue

                    raw_dist = levenshtein(w1, w2)
                    max_len = max(len(w1), len(w2))
                    normalized_dist = raw_dist / max_len if max_len > 0 else 0.0

                    results.append({
                        "topic": topic,
                        "language_pair": f"{lang_a}-{lang_b}",
                        "word_pair": [w1_original, w2_original],
                        "distance": round(normalized_dist, 4)
                    })

        self.word_distances = results
        return results

    def save_results(self) -> None:
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.word_distances, f, indent=2, ensure_ascii=False)

    def run(self) -> None:
        self.load_and_normalize_translations()
        self.compute_distances()
        self.save_results()

        print(f"\nWord distance analysis completed!")
        print(f"  Output → {self.output_path}")
        print(f"  Total word pairs analyzed: {len(self.word_distances)}")


def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    data_path = os.path.join(base_path, "data", "translated.json")
    output_path = os.path.join(base_path, "data", "analysis", "word_distance.json")

    analyzer = WordDistanceAnalyzer(data_path, output_path)
    analyzer.run()

if __name__ == "__main__":
    main()