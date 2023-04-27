from datetime import datetime
from typing import List
from urllib.request import urlopen

from requests_html import HTMLSession

from bs4 import BeautifulSoup

from src.common import ScrapedData


def scrape(url: str) -> ScrapedData:
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return ScrapedData(data=text, url=url, last_modified=datetime.now())


def crawl(url: str) -> List[ScrapedData]:
    pass


def scrape_aspx(url):
    # Create an HTML session and render the JavaScript code
    session = HTMLSession()
    response = session.get(url)
    response.html.render()

    # Find all the URLs in the rendered HTML
    urls = [link for link in response.html.links if link.startswith('http')]

    return urls

if __name__ == '__main__':
    res = scrape("https://www.gov.il/he/Departments/publications/?OfficeId=e744bba9-d17e-429f-abc3-50f7a8a55667&blockCollector=true&limit=10&publicationType=06311039-a4dc-4457-af46-a8e7dbfbe5a0&skip=0")

