import json
import os
from typing import Dict, List

WORD_DISTANCES_FILE = "../../../data/analysis/word_distance.json"
TOPIC_GRAPH_FILE = "../../../data/analysis/topic_proximity.json"
OUTPUT_DIR = "../../../data/analysis"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "outliers.json")

# Outlier if word distance > multiplier × topic distance
OUTLIER_MULTIPLIER = 2.5
MIN_TOPIC_DISTANCE = 0.01

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================= LOAD DATA =========================
with open(WORD_DISTANCES_FILE, 'r', encoding='utf-8') as f:
    word_distances: List[Dict] = json.load(f)

print(f"Loaded {len(word_distances)} word pairs.")

with open(TOPIC_GRAPH_FILE, 'r', encoding='utf-8') as f:
    raw_topic_graph = json.load(f)

# ========================= BUILD TOPIC DISTANCE LOOKUP =========================
topic_distance_map = {}


def get_lang(code: str) -> str:
    return code.split('_')[-1]


for topic_name, topic_data in raw_topic_graph.items():
    topic_key = topic_name.strip().lower()
    edges = topic_data.get("edges", [])

    dist_lookup = {}
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]
        weight = edge["weight"]

        lang1 = get_lang(src)
        lang2 = get_lang(tgt)

        pair = tuple(sorted([lang1, lang2]))
        pair_key = f"{pair[0]}-{pair[1]}"
        dist_lookup[pair_key] = weight

    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]
        weight = edge["weight"]
        lang1 = get_lang(src)
        lang2 = get_lang(tgt)
        pair_forward = f"{lang1}-{lang2}"
        pair_reverse = f"{lang2}-{lang1}"
        normalized = f"{min(lang1, lang2)}-{max(lang1, lang2)}"

        actual_weight = dist_lookup[normalized]

        topic_distance_map[(topic_key, pair_forward)] = actual_weight
        topic_distance_map[(topic_key, pair_reverse)] = actual_weight

print(f"Loaded topic distances for {len(topic_distance_map)} topic-language pairs.")

# ========================= DETECT OUTLIERS =========================
outliers = []

for item in word_distances:
    topic = item["topic"].lower()
    lang_pair = item["language_pair"]  # e.g. "en-es"
    word_pair = item["word_pair"]  # [word1, word2]
    distance = item["distance"]

    key = (topic, lang_pair)
    topic_dist = topic_distance_map.get(key)

    if topic_dist is None:
        l1, l2 = lang_pair.split('-')
        reverse_pair = f"{l2}-{l1}"
        key_rev = (topic, reverse_pair)
        topic_dist = topic_distance_map.get(key_rev)

    if topic_dist is None:
        print(f"Warning: No topic distance for {topic} | {lang_pair} → skipping {word_pair}")
        continue

    if topic_dist < MIN_TOPIC_DISTANCE:
        continue

    ratio = distance / topic_dist if topic_dist > 0 else float('inf')

    if distance > topic_dist * OUTLIER_MULTIPLIER:
        outliers.append({
            "topic": topic,
            "language_pair": lang_pair,
            "word_pair": word_pair,
            "distance": round(distance, 4),
            "topic_distance": round(topic_dist, 4),
            "ratio": round(ratio, 2)
        })

outliers.sort(key=lambda x: x["ratio"], reverse=True)

# ========================= SAVE RESULT =========================
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

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

print(f"\nFound {len(outliers)} outliers.")
print(f"Saved to: {OUTPUT_FILE}")