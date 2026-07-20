import json
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "chroma_db"
COLLECTION_NAME = "sports_facts"


def get_client():
    """Create or connect to the local ChromaDB database."""
    return chromadb.PersistentClient(path=DB_PATH)


def get_collection():
    """Create or retrieve the collection."""
    client = get_client()

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    return collection

import os


def populate_database(json_path="data/sports_facts.json"):
    """
    Read the JSON dataset and insert all facts into ChromaDB.
    """

    collection = get_collection()

    # Prevent duplicate insertion
    if collection.count() > 0:
        print(f"Database already contains {collection.count()} documents.")
        return

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found.")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    metadatas = []
    ids = []

    for item in data:
        documents.append(item["fact"])

        metadatas.append({
            "sport": item["sport"],
            "category": item["category"],
            "difficulty": item["difficulty"]
        })

        ids.append(str(item["id"]))

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully inserted {len(documents)} documents.")

def query_database(query_text, n_results=5, sport=None, difficulty=None):
    """
    Search ChromaDB using semantic similarity.
    Supports sport and difficulty filtering.
    """

    collection = get_collection()

    # Build filters
    filters = []

    if sport:
        filters.append({"sport": sport})

    if difficulty:
        filters.append({"difficulty": difficulty})

    # Apply filters correctly for ChromaDB
    if len(filters) == 1:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=filters[0]
        )

    elif len(filters) > 1:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={
                "$and": filters
            }
        )

    else:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

    return results