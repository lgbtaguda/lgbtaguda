from scraping.tools import scrape, scrape_aspx
from chatbot import ask_if_affects_lgbt
from common import BECallable, URLS
from scraping.file_parsing import read_pdf
import time
import asyncio
from pathlib import Path
import json


async def main():
    start_time = time.time()
    for url in URLS.values():
        list_of_urls = await scrape_aspx(url)
        for url in list_of_urls:
            scraped = scrape(url)
            if scraped.data:
                if len(scraped.data) > 100:
                    result = ask_if_affects_lgbt(scraped.data)
                    print(scraped.data[:200] + " ...")
                    print(f"Link:\n {scraped.url} \nIs The Data Problematic?:\n {result}")
        if (time.time() - start_time) / 60 > 1.5:
            break

BE_SCRAPE_MAPPING = {"knesset": BECallable(callable_method=BECallable.parse_knesset, args=[], url=URLS['hakika']),
                     "read from pdf": BECallable(callable_method=read_pdf, args=['pdf_path'], url=""),
                     "read from website": BECallable(callable_method=scrape, args=['url'], url="")
                     }
# BE_SCRAPE_MAPPING[called_method].callable_method(**kwargs)
BE_ANALYZE_MAPPING = {}

if __name__ == "__main__":
    asyncio.run(main())
