import os
import json
import threading
import itertools
import time
import sys
from modules.scraper import Scraper, PageFetcher, PageParser, TextProcessor, TextStorage, Topic
from modules.translator import WordTranslator
from modules.analysis.global_proximity import GlobalProximityAnalyzer
from modules.analysis.topic_analysis import TopicAnalyzer
from modules.analysis.word_distance import WordDistanceAnalyzer
from modules.analysis.community_detection import CommunityDetector
from modules.analysis.outlier_detection import OutlierDetector

class LoadingSpinner:
    def __init__(self, message="Processing..."):
        self.message = message
        self.stop_running = False
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])

    def spin(self):
        while not self.stop_running:
            sys.stdout.write(f"\r{self.message} {next(self.spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

    def __enter__(self):
        self.stop_running = False
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_running = True
        self.thread.join()

class Pipeline:
    def __init__(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.base_path, "data")
        self.analysis_dir = os.path.join(self.data_dir, "analysis")
        self.config_path = os.path.join(self.base_path, "app", "config.json")

        self.scrapped_file = os.path.join(self.data_dir, "scrapped.txt")
        self.translated_file = os.path.join(self.data_dir, "translated.json")
        self.global_proximity_file = os.path.join(self.analysis_dir, "global_proximity.json")
        self.topic_proximity_file = os.path.join(self.analysis_dir, "topic_proximity.json")
        self.word_distance_file = os.path.join(self.analysis_dir, "word_distance.json")
        self.communities_file = os.path.join(self.analysis_dir, "communities.json")
        self.outliers_file = os.path.join(self.analysis_dir, "outliers.json")

        self.scraped_data = None
        self.scraped_data_objects = None

    def run_scraper(self):
        print("\n=== Step 1: Scraping ===")
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            
            topics = [Topic(url=item["url"], title=item["title"]) for item in config["topics"]]

            with LoadingSpinner("Scraping topics..."):
                scraper = Scraper(
                    topics, 
                    fetcher=PageFetcher(), 
                    parser=PageParser(), 
                    processor=TextProcessor(), 
                    storage=TextStorage()
                )
                self.scraped_data_objects = scraper.run()

            self.scraped_data = [
                {"topic": item.topic, "words": item.words} 
                for item in self.scraped_data_objects
            ]
            
            print(f"Scraping completed. Collected {len(self.scraped_data)} topics.")
        except Exception as e:
            print(f"Scraping failed: {e}")
            raise

    def run_translator(self):
        print("\n=== Step 2: Translation ===")
        if not hasattr(self, 'scraped_data'):
            raise ValueError("Scraped data not found. Run scraper first.")
            
        translator = WordTranslator()
        with LoadingSpinner("Translating words..."):
            translator.process(
                output_file=self.translated_file,
                input_data=self.scraped_data
            )

    def run_analysis(self):
        print("\n=== Step 3: Analysis ===")

        print("Running Global Proximity Analysis...")
        with LoadingSpinner("Computing global proximity..."):
            global_analyzer = GlobalProximityAnalyzer(self.translated_file, self.global_proximity_file)
            global_analyzer.run()

        print("Running Topic Analysis...")
        with LoadingSpinner("Computing topic analysis..."):
            topic_analyzer = TopicAnalyzer(self.translated_file, self.topic_proximity_file)
            topic_analyzer.run()

        print("Running Word Distance Analysis...")
        with LoadingSpinner("Computing word distances..."):
            word_analyzer = WordDistanceAnalyzer(self.translated_file, self.word_distance_file)
            word_analyzer.run()


        print("Running Community Detection...")
        with LoadingSpinner("Detecting communities..."):
            community_detector = CommunityDetector(self.topic_proximity_file, self.communities_file)
            community_detector.run()

        print("Running Outlier Detection...")
        with LoadingSpinner("Detecting outliers..."):
            outlier_detector = OutlierDetector(
                word_distances_path=self.word_distance_file,
                topic_graph_path=self.topic_proximity_file,
                output_dir=self.analysis_dir
            )
            outlier_detector.run()

    def run(self):
        self.run_scraper()
        self.run_translator()
        self.run_analysis()
        print("\n=== Pipeline Completed Successfully ===")

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
