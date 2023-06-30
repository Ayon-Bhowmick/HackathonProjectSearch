# Hackathon Project Search

## Description

This project was made in order to help me and my friends come up with a project idea for a hackathon. It uses a vector database to preform a semantic search on all previous winning hackathon projects to give ideas on new ones. The descriptions of the winning hackathon projects was scraped from [Devpost](https://devpost.com/).

## How to use

1. `py WebScraper.py` to scrape the project descriptions from Devpost
2. `py VectorDB.py` to embed the project descriptions and store them in a vector database
3. `py DiscordBot.py` lets you preform queries on the database using a discord bot or `uvicorn api:api --reload` lets you query the database though a REST API

## Sources

- The descriptions of the winning hackathon projects was scraped from [Devpost](https://devpost.com/) using [Selenium](https://www.selenium.dev/).
- The projects descriptions were embedded using [All MPNet base V2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) which is a fine tuned version of Microsoft's [MPNet](https://huggingface.co/microsoft/mpnet-base).
- The vector database was made using [Chroma](https://www.trychroma.com/) which is built on top of DuckDB and Apache Parquet.
- The discord bot was made using [Discord.py](https://discordpy.readthedocs.io/en/stable/) and the REST API was made using [FastAPI](https://fastapi.tiangolo.com/).
