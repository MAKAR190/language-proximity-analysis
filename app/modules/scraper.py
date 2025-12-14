import json, requests, os, lxml
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bs4 import BeautifulSoup

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

class PageFetcher(IFetcher):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    def fetch(self, topic: Topic) -> str:
        page = requests.get(topic.url, headers=self.headers, allow_redirects=True)
        return page.text

class PageParser(IParser):
    MAX_WORDS = 100
    def parse(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        words = []
        for li in soup.select("span.term a"):
            if len(words) >= self.MAX_WORDS:
                 break
            text = li.get_text(strip=True)
            if text and len(text.split()) == 1:
                words.append(text)

        return words

class TextProcessor(IProcessor):
    def process(self, words: list[str]) -> list[str]:
        return sorted(set(w.lower() for w in words))

class TextStorage(IStorage):
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    def __init__(self):
        self._file_initialized = False

    def store(self, topic: Topic, words: list[str]) -> None:
        os.makedirs(self.DATA_DIR, exist_ok=True)
        path = os.path.join(self.DATA_DIR, "scrapped.txt")
        mode = "a+" if self._file_initialized else "w+"
        self._file_initialized = True

        with open(path, mode, encoding="utf-8") as scrapped_file:
            scrapped_file.write(f"Topic: {topic.title}\n{words}\n\n")

class Scraper:
    def __init__(self, topics: list[Topic],  fetcher: IFetcher,
                 parser: IParser,
                 processor: IProcessor,
                 storage: IStorage):
        self.topics = TopicsInput(topics)
        self.fetcher = fetcher
        self.parser = parser
        self.processor = processor
        self.storage = storage
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
        for t in self.topics:
            html = self.fetcher.fetch(t)
            words = self.parser.parse(html)
            processed_words = self.processor.process(words)
            self.storage.store(t, processed_words)
            self.output.append(TopicOutput(topic=t.title, words=processed_words))
        return self._output

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.json")) as f:
        data = json.load(f)

    try:
        config_topics = [Topic(url=item["url"], title=item["title"]) for item in data["topics"]]
    except KeyError:
        raise KeyError("Missing 'topics' key in config.json")

    scraper = Scraper(config_topics, fetcher=PageFetcher(), parser=PageParser(), processor=TextProcessor(), storage=TextStorage())
    scraper.run()