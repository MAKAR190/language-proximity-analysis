 # Input: topics
 # Output: [ { topic: "Fruits", words: [{ word: "apple" }, ...], ... } ]

# ├─ fetcher: IFetcher → WikipediaFetcher / NewsFetcher
# ├─ parser: IParser → HTMLParser / JSONParser
# ├─ processor: IProcessor → TextProcessor
# └─ storage: IStorage → JSONStorage / DatabaseStorage

import json, requests, os
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Types and Interfaces
@dataclass
class Topic:
    url: str
    title: str
@dataclass(frozen=True)
class TopicsInput:
    topics: list[Topic]

    def __iter__(self):
        return iter(self.topics)
    def __getitem__(self, index):
        return self.topics[index]
    def __len__(self):
        return len(self.topics)
@dataclass
class TopicOutput:
    topic: str
    words: list[str]
class IFetcher(ABC):
    @abstractmethod
    def fetch(self, topic: Topic) -> str:
        pass
class IParser(ABC):
    @abstractmethod
    def parse(self, raw_data: str) -> list[str]:
        pass
class IProcessor(ABC):
     @abstractmethod
     def process(self, words: list[str]) -> list[str]:
         pass
class IStorage(ABC):
    @abstractmethod
    def store(self, topic: Topic, words: list[str]) -> None:
        pass
# -------------------------

class WikipediaFetcher(IFetcher):
    def fetch(self, topic: Topic) -> str:
        pass

class WikipediaParser(IParser):
    def parse(self, raw_data: str) -> list[str]:
        pass

class TextProcessor(IProcessor):
    def process(self, words: list[str]) -> list[str]:
        pass

class JSONStorage(IStorage):
    def store(self, topic: Topic, words: list[str]) -> None:
        pass

class Scraper:
    def __init__(self, topics: list[Topic]):
        self.topics = TopicsInput(topics)
        self._output: list[TopicOutput] = []

    @property
    def output(self):
        return self._output
    @output.setter
    def output(self, value: list[TopicOutput]):
        if not all(isinstance(item, TopicOutput) for item in value):
            raise TypeError("All items in output must be type of TopicOutput!")
        self._output = value

    def run(self):
        pass

if __name__ == "__main__":
    # Importing topics config for independent single module testing
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.json")) as f:
        data = json.load(f)

    try:
        config = data["topics"]
    except KeyError:
        raise KeyError("Missing 'topics' key in config.json")

    scraper = Scraper(config)
    scraper.run()