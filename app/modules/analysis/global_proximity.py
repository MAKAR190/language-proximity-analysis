# What to implement:

# Calculate the average Levenshtein distance for each pair of languages,
# aggregated across all topics and all words in the global corpus.

# Generate a single JSON file at data/analysis/global_proximity.json that contains
# a distance matrix mapping each language pair to their average distance value.

# The output should look like this example structure:
# {
#   "global_distances": {
#     "english-french": 2.34,
#     "english-german": 2.89,
#     "french-german": 1.95,
#     ...
#   }
# }

# Visualization: Use GraphStream in Java GUI (GlobalProximityGraph.java) to display
# a network graph where each node represents a language, and edges between nodes
# are weighted by the average distance (thicker edges = closer languages,
# thinner edges = more distant).

# This addresses the research question on the general proximity of languages
# based on the global corpus.

# ----------------------------------------------------------------------------------

import json
import os
import itertools
from typing import List, Dict
from statistics import mean

from common_functions import levenshtein, normalize, load_translations 

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
TRANSLATIONS_PATH = os.path.join(BASE_PATH, "translated.json")
OUTPUT_PATH = os.path.join(BASE_PATH, "analysis", "global_proximity.json")


def compute_global_distances(translated_data: List[Dict]) -> Dict:
    """
    Calculate the average Levenshtein distances for all pairs of languages on all topics.
    """
    # Define languages dynamically by the first word.
    languages = [lang for lang in translated_data[0]["words"][0].keys() if lang != "topic"]
    lang_pairs = list(itertools.combinations(languages, 2))

    # A dictionary for accumulating distances
    distances_acc = {f"{lang_a}-{lang_b}": [] for lang_a, lang_b in lang_pairs}

    for topic_entry in translated_data:
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

    # The average distance for each pair of languages
    global_distances = {}
    for pair, values in distances_acc.items():
        if values:
            avg_distance = mean(values)
            # Weights from 0 to 1 (the smaller the distance, the closer the languages are)
            weight = round(1 - avg_distance, 4)
            lang_a, lang_b = pair.split("-")
            key = f"{lang_a}-{lang_b}"
            global_distances[key] = weight

    # Preparing JSON in the form of "nodes" and "edges" for possible visualization
    nodes = [{"id": lang} for lang in languages]
    edges = []
    for pair, weight in global_distances.items():
        lang_a, lang_b = pair.split("-")
        edges.append({"source": lang_a, "target": lang_b, "weight": weight})

    return {"language": {"nodes": nodes, "edges": edges}}


def save_global_distances(global_data: Dict, output_path: str = OUTPUT_PATH):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(global_data, f, indent=2, ensure_ascii=False)


def run_global_proximity():
    dataset = load_translations(TRANSLATIONS_PATH)
    global_data = compute_global_distances(dataset)
    save_global_distances(global_data)
    print(f"Global proximity computed and saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    run_global_proximity()
