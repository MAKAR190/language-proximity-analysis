import json
import requests
from typing import List, Dict, Any

class WordTranslator:
    
    def __init__(self, api_url: str = "http://127.0.0.1:5000/translate"):
        self.api_url = api_url
        self.source_language = "en"
        self.target_languages = ["es", "fr", "de", "it", "pt"]
    
    def read_input_data(self, input_file: str) -> List[Dict[str, Any]]:
        with open(input_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def translate_word(self, word: str, source: str, target: str) -> str:
        params = {
            'q': word,
            'source': source,
            'target': target,
            'format': "text",
            'api_key': ""
        }
        
        try:
            response = requests.post(self.api_url, params=params)
            response.raise_for_status()

            result = response.json()
            return result.get('translatedText', word)
        except Exception as e:
            print(f"Error translating '{word}' to {target}: {e}")
            return word
    
    def translate_topics(self, topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        translated_topics = []
        
        for topic in topics:
            print(f"\n--- Translating {topic['topic']} ---")
            
            translated_words = []
            for word in topic['words']:
                print(f"Translating: {word}")
                
                translations = {}
                for target_lang in self.target_languages:
                    translation = self.translate_word(word, self.source_language, target_lang)
                    translations[target_lang] = translation
                    print(f"  {target_lang}: {translation}")
                
                translated_words.append({
                    "original": word,
                    "translations": translations
                })
            
            translated_topics.append({
                "topic": topic['topic'],
                "words": translated_words
            })
        
        return translated_topics
    
    def create_output_structure(self, translated_topics: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "source_language": self.source_language,
            "target_languages": self.target_languages,
            "topics": translated_topics
        }
    
    def save_output(self, data: Dict[str, Any], output_file: str):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Translation complete! Output saved to: {output_file}")
    
    def process(self, input_file: str, output_file: str):
        print(f"Reading data from: {input_file}")
        topics = self.read_input_data(input_file)
        
        print(f"\nTranslating words to: {', '.join(self.target_languages)}")
        translated_topics = self.translate_topics(topics)
        
        output_data = self.create_output_structure(translated_topics)
        
        self.save_output(output_data, output_file)


if __name__ == "__main__":
    translator = WordTranslator(api_url="http://127.0.0.1:5000/translate")

    translator.process(
        input_file="../../data/testData.json",
        output_file="../../data/translated.json"
    )