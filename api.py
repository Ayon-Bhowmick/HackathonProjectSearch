from fastapi import FastAPI, Response, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from pydantic import BaseModel


class QueryBody(BaseModel):
    question: str
    num_res: int

api = FastAPI()
# make collection
ef = embedding_functions.InstructorEmbeddingFunction(model_name="sentence-transformers/all-mpnet-base-v2", device="cuda") # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
collection = client.get_or_create_collection(name="projects", embedding_function=ef, metadata={"hnsw:space": "cosine"})

@api.get("/query")
def query(question: str = Body(..., embed=True), num_res: int = Body(..., embed=True)):
    res = collection.query(query_texts=[question], n_results=num_res)
    return res
