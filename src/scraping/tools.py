from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
# from selenium import webdriver

from common import ScrapedData


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


# class Parser:
#     def __init__(self):
#         self.session = HTMLSession()
#
#     def get(self, url):
#         self.response = self.session.get(url)

async def render_js(url):
    # session = HTMLSession()
    session = AsyncHTMLSession()
    response = await session.get(url)
    # response.html.render()
    await response.html.arender()
    return response.html


async def scrape_aspx(url):
    # Create an HTML session and render the JavaScript code
    # session = HTMLSession()
    session = AsyncHTMLSession()

    response = await session.get(url)
    await response.html.arender()

    # Find all the URLs in the rendered HTML
    urls = [link for link in response.html.links if link.startswith('http')]

    return urls


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"


# def parse_chrome(url):
#     # driver = webdriver.Chrome()
#     options = webdriver.ChromeOptions()
#
#     options.add_argument("--enable-javascript")
#     options.add_argument(f'user-agent={user_agent}')
#
#     driver = webdriver.Chrome(chrome_options=options)
#     driver.get(url)
#     driver.current_url
#     htmlSource = driver.page_source
#     print(1)


if __name__ == '__main__':
    # parse_chrome('https://main.knesset.gov.il/about/departments/pages/sg/sgpresidium.aspx')
    res = scrape_aspx(
        "https://www.gov.il/he/Departments/publications/?OfficeId=e744bba9-d17e-429f-abc3-50f7a8a55667&blockCollector=true&limit=10&publicationType=06311039-a4dc-4457-af46-a8e7dbfbe5a0&skip=0")
