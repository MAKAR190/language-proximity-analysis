import json
import requests
from typing import List, Dict, Any
import re
import uuid
from dotenv import load_dotenv
import os

class WordTranslator:

    def __init__(self):
        base_dir = os.path.dirname(__file__)
        env_path = os.path.join(base_dir, "../.env.local")
        config_path = os.path.join(base_dir, "../config.json")

        load_dotenv(env_path)
        self.source_language = "en"
        self.api_key = os.getenv("TRANSLATE_API_KEY")
        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"
        self.location = os.getenv("TRANSLATE_LOCATION")
        self.constructed_url = self.endpoint
        self.target_languages = self._read_languages_from_config(config_path)

        # Configure retry strategy
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _read_languages_from_config(self, config_file: str) -> List[str]:
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("languages", ["es", "fr", "pl"])
        except Exception as e:
            print(f"Error reading config file: {e}. Using default languages.")
            return ["es", "fr", "pl"]

    def read_input_data(self, input_file: str) -> List[Dict[str, Any]]:
        if input_file.endswith('.txt'):
            return self._read_txt_format(input_file)
        else:
            return self._read_json_format(input_file)

    def _read_json_format(self, input_file: str) -> List[Dict[str, Any]]:
        with open(input_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _read_txt_format(self, input_file: str) -> List[Dict[str, Any]]:
        topics = []

        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        topic_blocks = re.split(r'Topic:\s*', content)

        for block in topic_blocks:
            block = block.strip()
            if not block:
                continue

            lines = block.split('\n', 1)

            if len(lines) < 2:
                continue

            topic_name = lines[0].strip()
            words_str = lines[1].strip()

            try:
                words = eval(words_str)
                if isinstance(words, list):
                    topics.append({
                        "topic": topic_name,
                        "words": words
                    })
            except Exception as e:
                print(f"Error parsing words for topic '{topic_name}': {e}")
                continue

        return topics

    def translate_word(self, word: str, source: str, target: str) -> str:
        params = {
            'api-version': '3.0',
            'from': source,
            'to': target
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': word
        }]

        try:
            response = self.session.post(self.constructed_url, params=params, headers=headers, json=body)
            response.raise_for_status()

            result = response.json()
            if result and len(result) > 0 and 'translations' in result[0]:
                return result[0]['translations'][0]['text']
            return word
        except Exception as e:
            print(f"Error translating '{word}' to {target}: {e}")
            return word

    def translate_topics(self, topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        translated_topics = []

        for topic in topics:
            print(f"\n--- Translating {topic['topic']} ---")

            translated_words = []
            for word in topic['words']:

                word_translations = {self.source_language: word}
                for target_lang in self.target_languages:
                    translation = self.translate_word(word, self.source_language, target_lang)
                    word_translations[target_lang] = translation

                translated_words.append(word_translations)

            translated_topics.append({
                "topic": topic['topic'],
                "words": translated_words
            })

        return translated_topics

    def save_output(self, data: Dict[str, Any], output_file: str):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Translation complete! Output saved to: {output_file}")

    def process(self, output_file: str, input_file: str = None, input_data: List[Dict[str, Any]] = None):
        if os.path.exists(output_file):
            print(f"Output file '{output_file}' already exists. Skipping translation to save API tokens.")
            return

        if input_data:
            print("Using provided input data.")
            topics = input_data
        elif input_file:
            print(f"Reading data from: {input_file}")
            topics = self.read_input_data(input_file)
        else:
            raise ValueError("Either input_file or input_data must be provided.")

        print(f"\nTranslating words to: {', '.join(self.target_languages)}")
        translated_topics = self.translate_topics(topics)

        self.save_output(translated_topics, output_file)


if __name__ == "__main__":
    translator = WordTranslator()

    translator.process(
        input_file="../../data/scrapped.txt",
        output_file="../../data/translated.json"
    )