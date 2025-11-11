# Output format description:

# The JSON file `data/analysis/outliers.json` should be a structured list of objects,
# each representing an outlier word pair detected within a specific topic and language pair.

# Example JSON output:
# {
#   "outliers": [
#     {
#       "topic": "animals",
#       "language_pair": "english-german",
#       "word_pair": ["mouse", "maus"],
#       "distance": 4.2
#     },
#     {
#       "topic": "technology",
#       "language_pair": "french-german",
#       "word_pair": ["ordinateur", "computer"],
#       "distance": 7.8
#     }
#   ]
# }

# This detailed output allows your Java GUI visualization to size and color nodes
# based on the severity of the anomaly (z_score), as well as provide tooltip or
# label information with precise distance metrics.

# It also supports optional analysis or explanations in reports or interactive UI.