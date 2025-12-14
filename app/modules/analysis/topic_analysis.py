import os
import itertools
import json
from statistics import mean
from .common_functions import normalize, levenshtein, load_translations

class TopicAnalyzer:
    def __init__(self, data_path: str, output_path: str):
        self.data_path = data_path
        self.output_path = output_path
        self.translated_data = None
        self.results = None

    def load_data(self):
        self.translated_data = load_translations(self.data_path)

    def compute_distances(self):
        self.results = {}

        for topic_entry in self.translated_data:
            topic = topic_entry["topic"]
            words = topic_entry["words"]

            languages = [lang for lang in words[0].keys() if lang != "topic"]
            pair_distances = {f"{a}-{b}": [] for a,b in itertools.combinations(languages,2)}
            max_word_length = {}

            for word_entry in words:
                for lang_a, lang_b in itertools.combinations(languages,2):
                    w1 = normalize(word_entry.get(lang_a))
                    w2 = normalize(word_entry.get(lang_b))
                    if not w1 or not w2:
                        continue
                    dist = levenshtein(w1, w2)
                    normalized_dist = dist / max(len(w1), len(w2))
                    key = f"{lang_a}-{lang_b}"
                    pair_distances[key].append(normalized_dist)
                    max_word_length[key] = max(max_word_length.get(key,0), len(w1), len(w2))

            nodes = [{"id": f"{topic.lower()}_{lang}"} for lang in languages]
            edges = []
            for lang_a, lang_b in itertools.combinations(languages,2):
                key = f"{lang_a}-{lang_b}"
                distances = pair_distances.get(key,[])
                if not distances:
                    continue
                mean_distance = mean(distances)
                weight = 1 - mean_distance
                edges.append({
                    "source": f"{topic.lower()}_{lang_a}",
                    "target": f"{topic.lower()}_{lang_b}",
                    "weight": round(weight,4)
                })

            self.results[topic] = {
                "nodes": nodes,
                "edges": edges
            }

    def save_results(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path,"w",encoding="utf-8") as f:
            json.dump(self.results,f,indent=4,ensure_ascii=False)

    def run(self):
        self.load_data()
        self.compute_distances()
        self.save_results()
        print("\nTopic proximity analysis completed!")
        print(f"Saved to: {self.output_path}")

def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    data_path = os.path.join(base_path,"data/translated.json")
    output_path = os.path.join(base_path,"data/analysis/topic_proximity.json")

    analyzer = TopicAnalyzer(data_path, output_path)
    analyzer.run()

if __name__=="__main__":
    main()
