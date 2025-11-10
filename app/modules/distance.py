### {
#    "word_graph": {
#        "nodes": [
#            {"id": "computer_EN", "label": "computer", "lang": "EN", "topic": "IT"},
#            {"id": "komputer_PL", "label": "komputer", "lang": "PL", "topic": "IT"},
#            {"id": "комп'ютер_UA", "label": "комп'ютер", "lang": "UA", "topic": "IT"},
#            {"id": "matrix_EN", "label": "matrix", "lang": "EN", "topic": "Math"},
#           {"id": "macierz_PL", "label": "macierz", "lang": "PL", "topic": "Math"},
#            {"id": "матриця_UA", "label": "матриця", "lang": "UA", "topic": "Math"}
#        ],
#        "links": [
#            {"source": "computer_EN", "target": "komputer_PL", "distance": 0.1},
#           {"source": "computer_EN", "target": "комп'ютер_UA", "distance": 0.2},
#            {"source": "komputer_PL", "target": "комп'ютер_UA", "distance": 0.15},
#           {"source": "matrix_EN", "target": "macierz_PL", "distance": 0.05},
#            {"source": "matrix_EN", "target": "матриця_UA", "distance": 0.08},
#           {"source": "macierz_PL", "target": "матриця_UA", "distance": 0.07}
#        ]
#   },
#    "topic_graph": {
#        "nodes": [
#            {"id": "IT", "label": "IT"},
#           {"id": "Math", "label": "Math"}
#        ],
#        "links": [
#            {"source": "IT", "target": "Math", "distance": 0.25}
#        ]
#    }
#}
#