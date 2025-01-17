import os
from uuid import uuid4
from qdrant_client import QdrantClient, models
from typing import List
from dotenv import load_dotenv

from lib import vector

load_dotenv()  # Load environment variables from .env file

qdrant_client = QdrantClient(
    api_key=os.getenv("CLAYSIS_API_KEY"),
    url=os.getenv("CLAYSIS_URL"),
)

print(qdrant_client.get_collections())


def initilize_coll():
    qdrant_client.create_collection(
        collection_name="docs",
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )


def insert_doc(text: str, name: str, embedding: List[float]):
    if not qdrant_client.collection_exists(collection_name="docs"):
        qdrant_client.create_collection(
            collection_name="docs",
            vectors_config=models.VectorParams(
                size=384, distance=models.Distance.COSINE
            ),
        )

    return qdrant_client.upsert(
        collection_name="docs",
        points=[
            models.PointStruct(
                id=str(uuid4()),
                payload={"text": text, "name": name},
                vector=embedding,
            ),
        ],
    )


async def retrieve(query: str):
    vec, _ = await vector.text_embed(query)
    search_queries = [
        models.SearchRequest(vector=vec, limit=4),
    ]
    res = qdrant_client.search_batch(collection_name="docs", requests=search_queries)
    result = qdrant_client.retrieve(
        collection_name="docs",
        ids=[item.id for item in res[0]],
    )
    return result
