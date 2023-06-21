import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os
import time

# make collection
ef = embedding_functions.InstructorEmbeddingFunction(model_name="sentence-transformers/all-mpnet-base-v2", device="cuda") # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
collection = client.get_or_create_collection(name="projects", embedding_function=ef, metadata={"hnsw:space": "cosine"})

if __name__ == "__main__":
    start = time.time()

    # add documents
    for i, project in enumerate(os.listdir("./Projects")):
        with open("./Projects/" + project, "r") as f:
            project_name = project[:-4]
            text = [line for line in f.read().split("\n")]
            num_lines = len(text)
            metadata = [{"project": project_name, "part": j} for j in range(num_lines)]
            ids = [f"{i}_{j}" for j in range(num_lines)]
        try:
            collection.add(documents=text, ids=ids, metadatas=metadata)
            print(f"Added {project_name} to collection")
        except chromadb.errors.IDAlreadyExistsError as IDerror:
            print(f"{project_name} already in collection")
            continue

    seconds = time.time() - start
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    hours = minutes // 60
    minutes = minutes - hours * 60
    print(f"Total time: {int(hours)}:{int(minutes)}:{seconds}")
