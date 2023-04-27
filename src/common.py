from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScrapedData:
    url: str
    data: str
    last_modified: datetime

