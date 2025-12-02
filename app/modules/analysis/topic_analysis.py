# What to implement:

# For each topic, calculate the Levenshtein distance for every word pair across each language pair.

# Compute statistical summaries per topic-language pair, including:
# - Mean distance (average lexical proximity)
# - Variance or standard deviation (measure of consistency)

# Output the results to data/analysis/topic_proximity.json in a structured format like:

# {
#     "animals": {
#       "english-french": {"mean": 2.1, "std_dev": 0.45},
#       "english-german": {"mean": 2.7, "std_dev": 0.52},
#       ...
#     },
#     "technology": {
#       "english-french": {"mean": 2.8, "std_dev": 0.6},
#       ...
#     },
#     ...
# }

# Visualization: Use GraphStream in the Java GUI (TopicProximityGraph.java) to render
# each topic as a separate heatmap-like network graph. Nodes represent languages,
# edges show average distances between language pairs per topic, with edge colors
# indicating variance (green = low variance/consistent, red = high variance/inconsistent).

# Provide a topic selector UI to switch between individual topic graphs, enabling
# users to observe how language similarity varies across semantic domains.

# This implementation directly addresses the analysis of differences in language
# proximity at the topic level.

# topic_analysis.py

# --------------------------------------------------------------------------
 # topic_analysis.py
import os
import itertools
import json
from typing import List, Dict
from statistics import mean
from common_functions import normalize, levenshtein, load_translations

# -----------------------------
#  Compute distances per topic
# -----------------------------
def compute_topic_distances(translated_data: List[Dict]) -> Dict:
    results = {}

    for topic_entry in translated_data:
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

        results[topic] = {
            "nodes": nodes,
            "edges": edges
        }

    return results

# -----------------------------
#  Save analysis to JSON
# -----------------------------
def save_results(output_path: str, results: Dict):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(results,f,indent=4,ensure_ascii=False)

# -----------------------------
#  Main runner
# -----------------------------
def run_topic_analysis():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    data_path = os.path.join(base_path,"data/translated.json")
    output_path = os.path.join(base_path,"data/analysis/topic_proximity.json")

    translated_data = load_translations(data_path)
    results = compute_topic_distances(translated_data)
    save_results(output_path, results)

    print("\nTopic proximity analysis completed!")
    print(f"Saved to: {output_path}")


if __name__=="__main__":
    run_topic_analysis()
