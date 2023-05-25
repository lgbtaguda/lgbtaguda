from fastapi import FastAPI

from src.scraping.knesset import parse_knesset

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/knesset")
async def knesset():
    return parse_knesset()
