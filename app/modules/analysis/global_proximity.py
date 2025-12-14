import json
import os
import itertools
from statistics import mean
from .common_functions import levenshtein, normalize, load_translations

class GlobalProximityAnalyzer:
    def __init__(self, data_path: str, output_path: str):
        self.data_path = data_path
        self.output_path = output_path
        self.translated_data = None
        self.global_data = None

    def load_data(self):
        self.translated_data = load_translations(self.data_path)

    def compute_distances(self):
        languages = [lang for lang in self.translated_data[0]["words"][0].keys() if lang != "topic"]
        lang_pairs = list(itertools.combinations(languages, 2))

        distances_acc = {f"{lang_a}-{lang_b}": [] for lang_a, lang_b in lang_pairs}

        for topic_entry in self.translated_data:
            for word_entry in topic_entry["words"]:
                for lang_a, lang_b in lang_pairs:
                    w1 = normalize(word_entry.get(lang_a))
                    w2 = normalize(word_entry.get(lang_b))
                    if not w1 or not w2:
                        continue
                    dist = levenshtein(w1, w2)
                    max_len = max(len(w1), len(w2))
                    normalized_dist = dist / max_len if max_len > 0 else 0
                    distances_acc[f"{lang_a}-{lang_b}"].append(normalized_dist)

        global_distances = {}
        for pair, values in distances_acc.items():
            if values:
                avg_distance = mean(values)
                weight = round(1 - avg_distance, 4)
                lang_a, lang_b = pair.split("-")
                key = f"{lang_a}-{lang_b}"
                global_distances[key] = weight

        nodes = [{"id": lang} for lang in languages]
        edges = []
        for pair, weight in global_distances.items():
            lang_a, lang_b = pair.split("-")
            edges.append({"source": lang_a, "target": lang_b, "weight": weight})

        self.global_data = {"language": {"nodes": nodes, "edges": edges}}

    def save_results(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.global_data, f, indent=2, ensure_ascii=False)

    def run(self):
        self.load_data()
        self.compute_distances()
        self.save_results()
        print(f"Global proximity computed and saved to {self.output_path}")

def main():
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
    TRANSLATIONS_PATH = os.path.join(BASE_PATH, "translated.json")
    OUTPUT_PATH = os.path.join(BASE_PATH, "analysis", "global_proximity.json")

    analyzer = GlobalProximityAnalyzer(TRANSLATIONS_PATH, OUTPUT_PATH)
    analyzer.run()

if __name__ == "__main__":
    main()
