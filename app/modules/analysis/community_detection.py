import json
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform, cosine
from pathlib import Path


class CommunityDetector:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = None
        self.topics = None
        self.topic_vectors = None
        self.distance_matrix = None
        self.clusters = None
        self.cluster_analysis = None

    def load_data(self):
        with open(self.input_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def extract_topic_features(self):
        self.topics = list(self.data.keys())
        self.topic_vectors = {}

        for topic in self.topics:
            edges = self.data[topic]['edges']
            weights = sorted([edge['weight'] for edge in edges])
            self.topic_vectors[topic] = np.array(weights)

    def compute_distance_matrix(self):
        n = len(self.topics)
        self.distance_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                topic_i = self.topics[i]
                topic_j = self.topics[j]

                vec_i = self.topic_vectors[topic_i]
                vec_j = self.topic_vectors[topic_j]

                dist = cosine(vec_i, vec_j)
                self.distance_matrix[i, j] = dist
                self.distance_matrix[j, i] = dist

    def perform_clustering(self, method='average'):
        condensed_dist = squareform(self.distance_matrix)
        linkage_matrix = linkage(condensed_dist, method=method)
        n_topics = len(self.topics)
        max_clusters = min(n_topics - 1, 6)

        best_num_clusters = 2

        if n_topics > 2:
            merge_distances = linkage_matrix[:, 2]
            threshold = np.percentile(merge_distances, 70)

            cluster_labels = fcluster(linkage_matrix, threshold, criterion='distance')
            best_num_clusters = len(np.unique(cluster_labels))

            if best_num_clusters < 2:
                best_num_clusters = 2
            elif best_num_clusters > max_clusters:
                best_num_clusters = max_clusters
                cluster_labels = fcluster(linkage_matrix, best_num_clusters, criterion='maxclust')
        else:
            cluster_labels = fcluster(linkage_matrix, best_num_clusters, criterion='maxclust')

        self.clusters = {}
        for topic, label in zip(self.topics, cluster_labels):
            if label not in self.clusters:
                self.clusters[label] = []
            self.clusters[label].append(topic)

    def analyze_language_pairs(self):
        self.cluster_analysis = []

        for cluster_id, topic_list in sorted(self.clusters.items()):
            all_edges = []
            for topic in topic_list:
                all_edges.extend(self.data[topic]['edges'])

            language_pair_weights = {}

            for edge in all_edges:
                source_lang = edge['source'].split('_')[-1]
                target_lang = edge['target'].split('_')[-1]

                pair = '-'.join(sorted([source_lang, target_lang]))

                if pair not in language_pair_weights:
                    language_pair_weights[pair] = []
                language_pair_weights[pair].append(edge['weight'])

            avg_weights = {
                pair: np.mean(weights)
                for pair, weights in language_pair_weights.items()
            }

            sorted_pairs = sorted(avg_weights.items(), key=lambda x: x[1], reverse=True)

            pair_topics = {}
            for pair, _ in sorted_pairs:
                pair_topics[pair] = topic_list

            self.cluster_analysis.append({
                'community_id': int(cluster_id),
                **pair_topics
            })

    def save_results(self):
        output = {
            'topic_communities': self.cluster_analysis
        }

        output_file = Path(self.output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

    def run(self):
        self.load_data()
        self.extract_topic_features()
        self.compute_distance_matrix()
        self.perform_clustering()
        self.analyze_language_pairs()
        self.save_results()


def main():
    INPUT = '../../../data/analysis/topic_proximity.json'
    OUTPUT = '../../../data/analysis/communities.json'

    clusterer = CommunityDetector(INPUT, OUTPUT)
    clusterer.run()


if __name__ == '__main__':
    main()