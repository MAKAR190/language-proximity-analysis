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

import json
import os
import itertools
import statistics
import unicodedata
from typing import Dict, List


# -----------------------------
#  Normalize words
# -----------------------------
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


# -----------------------------
#  Levenshtein distance
# -----------------------------
def levenshtein(a: str, b: str) -> int:
    """Compute Levenshtein distance between two strings."""
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


# -----------------------------
#  Load translations
# -----------------------------
def load_translations(data_path: str) -> List[Dict]:
    """Load translated topics/words from JSON."""
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
#  Compute distances per topic
# -----------------------------
def compute_topic_distances(translated_data: List[Dict]) -> Dict:
    """
    For each topic:
      – detect languages dynamically
      – compute normalized Levenshtein distances
      – calculate mean distance for each language pair
      – build fully connected graph (nodes + edges)
    """

    results = {}

    for topic_entry in translated_data:
        topic = topic_entry["topic"]
        words = topic_entry["words"]

        # Detect available languages from the first word block
        languages = [lang for lang in words[0].keys() if lang != "topic"]

        # Prepare dictionary for storing all distances per pair
        pair_distances = {f"{a}-{b}": [] for a, b in itertools.combinations(languages, 2)}

        # Prepare dict to track max word length per language pair
        max_word_length = {}

        # --- Collect all distances for all words ---
        for word_entry in words:
            for lang_a, lang_b in itertools.combinations(languages, 2):
                w1 = normalize(word_entry.get(lang_a))
                w2 = normalize(word_entry.get(lang_b))

                if not w1 or not w2:
                    continue

                # compute raw Levenshtein
                dist = levenshtein(w1, w2)

                # normalized 0..1 by word length
                max_len = max(len(w1), len(w2))
                normalized_dist = dist / max_len if max_len > 0 else 0

                key = f"{lang_a}-{lang_b}"
                pair_distances[key].append(normalized_dist)

                # Track maximum word length for later normalization
                max_word_length[key] = max(
                    max_word_length.get(key, 0),
                    len(w1),
                    len(w2)
                )

        # --- Build nodes structure ---
        nodes = [{"id": f"{topic.lower()}_{lang}"} for lang in languages]

        # --- Build edges (fully connected graph) ---
        edges = []

        for lang_a, lang_b in itertools.combinations(languages, 2):
            key = f"{lang_a}-{lang_b}"
            distances = pair_distances.get(key, [])

            if not distances:
                continue

            mean_distance = sum(distances) / len(distances)
            max_len = max_word_length.get(key, 1)

            # weight = similarity, so closer languages → higher weight
            weight = 1 - (mean_distance / 1)  # already normalized 0..1

            edges.append({
                "source": f"{topic.lower()}_{lang_a}",
                "target": f"{topic.lower()}_{lang_b}",
                "weight": round(weight, 4)
            })

        # Save topic results
        results[topic] = {
            "nodes": nodes,
            "edges": edges
        }

    return results



# -----------------------------
#  Save analysis to JSON
# -----------------------------
def save_results(output_path: str, results: Dict):
    """Save analysis results into JSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


# -----------------------------
#  Main runner
# -----------------------------
def run_topic_analysis():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    data_path = os.path.join(base_path, "data/translated.json")
    output_path = os.path.join(base_path, "data/analysis/topic_proximity.json")

    translated_data = load_translations(data_path)
    results = compute_topic_distances(translated_data)
    save_results(output_path, results)

    print("\nTopic proximity analysis completed!")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    run_topic_analysis()
