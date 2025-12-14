import json
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path


class OutlierDetector:
    def __init__(
            self,
            word_distances_path: str,
            topic_graph_path: str,
            output_dir: str = "../../../data/analysis",
            outlier_multiplier: float = 2.5,
            min_topic_distance: float = 0.01,
    ):
        self.word_distances_path = Path(word_distances_path)
        self.topic_graph_path = Path(topic_graph_path)
        self.output_dir = Path(output_dir)
        self.output_file = self.output_dir / "outliers.json"

        self.outlier_multiplier = outlier_multiplier
        self.min_topic_distance = min_topic_distance

        self.word_distances: List[Dict[str, Any]] = []
        self.topic_distance_map: Dict[Tuple[str, str], float] = {}

    def load_word_distances(self) -> None:
        """Load list of word translation distances."""
        with open(self.word_distances_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        self.word_distances = []
        for main_word, data in raw_data.items():
            topic = data["topic"]
            for edge in data["edges"]:
                source = edge["source"]
                target = edge["target"]
                weight = edge["weight"]

                # Extract languages from node IDs (format: word_lang)
                src_parts = source.split('_')
                tgt_parts = target.split('_')

                lang1 = src_parts[-1]
                lang2 = tgt_parts[-1]

                w1 = "_".join(src_parts[:-1])
                w2 = "_".join(tgt_parts[:-1])

                # Create consistent language pair key
                l1, l2 = sorted([lang1, lang2])
                lang_pair = f"{l1}-{l2}"

                word_pair = f"{w1} ({lang1}) - {w2} ({lang2})"
                distance = 1.0 - weight

                self.word_distances.append({
                    "topic": topic,
                    "language_pair": lang_pair,
                    "word_pair": word_pair,
                    "distance": distance
                })

        print(f"Loaded {len(self.word_distances)} word pairs.")

    def load_and_parse_topic_graph(self) -> None:
        with open(self.topic_graph_path, 'r', encoding='utf-8') as f:
            raw_graph = json.load(f)

        def get_lang(node_id: str) -> str:
            return node_id.strip().split('_')[-1]

        for topic_name, topic_data in raw_graph.items():
            topic_key = topic_name.strip().lower()
            edges = topic_data.get("edges", [])

            normalized_distances: Dict[str, float] = {}
            for edge in edges:
                lang1 = get_lang(edge["source"])
                lang2 = get_lang(edge["target"])
                weight = edge["weight"]
                # Convert weight (similarity) to distance
                distance = 1.0 - weight

                pair_key = f"{min(lang1, lang2)}-{max(lang1, lang2)}"
                normalized_distances[pair_key] = distance

            # Second pass: store both directions
            for edge in edges:
                lang1 = get_lang(edge["source"])
                lang2 = get_lang(edge["target"])
                normalized_pair = f"{min(lang1, lang2)}-{max(lang1, lang2)}"
                distance = normalized_distances[normalized_pair]

                forward = f"{lang1}-{lang2}"
                reverse = f"{lang2}-{lang1}"

                self.topic_distance_map[(topic_key, forward)] = distance
                self.topic_distance_map[(topic_key, reverse)] = distance

        print(f"Built topic distance map with {len(self.topic_distance_map)} entries.")

    def find_topic_distance(self, topic: str, lang_pair: str) -> Optional[float]:
        key = (topic, lang_pair)
        if key in self.topic_distance_map:
            return self.topic_distance_map[key]

        l1, l2 = lang_pair.split('-')
        reverse_pair = f"{l2}-{l1}"
        rev_key = (topic, reverse_pair)
        return self.topic_distance_map.get(rev_key)

    def detect_outliers(self) -> List[Dict[str, Any]]:
        outliers = []

        for item in self.word_distances:
            topic = item["topic"].lower()
            lang_pair = item["language_pair"]
            word_pair = item["word_pair"]
            distance = item["distance"]

            topic_dist = self.find_topic_distance(topic, lang_pair)

            if topic_dist is None:
                print(f"  Warning: No topic distance for '{topic}' | {lang_pair} → skipping {word_pair}")
                continue

            if topic_dist < self.min_topic_distance:
                continue

            ratio = distance / topic_dist

            if distance > topic_dist * self.outlier_multiplier:
                outliers.append({
                    "topic": topic,
                    "language_pair": lang_pair,
                    "word_pair": word_pair,
                    "distance": round(distance, 4),
                    "topic_distance": round(topic_dist, 4),
                    "ratio": round(ratio, 2)
                })

        outliers.sort(key=lambda x: x["ratio"], reverse=True)
        return outliers

    def save_results(self, outliers: List[Dict[str, Any]]) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        final_output = {
            "outliers": [
                {
                    "topic": o["topic"],
                    "language_pair": o["language_pair"],
                    "word_pair": o["word_pair"],
                    "distance": o["distance"]
                }
                for o in outliers
            ]
        }

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)

        print(f"\nFound {len(outliers)} outliers.")
        print(f"Results saved to: {self.output_file}")

    def run(self) -> None:
        self.load_word_distances()
        self.load_and_parse_topic_graph()
        outliers = self.detect_outliers()
        self.save_results(outliers)


if __name__ == "__main__":
    detector = OutlierDetector(
        word_distances_path="../../../data/analysis/word_distance.json",
        topic_graph_path="../../../data/analysis/topic_proximity.json",
        outlier_multiplier=2.5,
        min_topic_distance=0.01
    )
    detector.run()