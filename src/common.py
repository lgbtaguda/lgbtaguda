from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.request import urlopen
import json
from pathlib import Path
import os
from bs4 import BeautifulSoup

urls_file = os.path.join(os.path.dirname(__file__), "data\\urls.json")
keywords_path = os.path.join(os.path.dirname(__file__), "data\\keywords.txt")

with open(urls_file) as f:
    URLS = json.load(f)["urls_for_scraping"]

with open(keywords_path, "r", encoding="utf-8") as f:
    KEYWORDS = f.read().split("\n")
# KEYWORDS = (keywords_path).read_text().split("\n")  # careful not to end file with blank line.

@dataclass
class ScrapedData:
    url: str
    data: str
    last_modified: datetime = datetime.now()


@dataclass
class AnalyzedData:
    data: str
    last_modified: datetime

@dataclass
class BECallable:
    callable_method: callable
    args: list
    url: str

    def parse_knesset(self) -> List[ScrapedData]:
        html = urlopen(self.url).read()
        soup = BeautifulSoup(html, features="html.parser")
        return soup



