from fastapi import UploadFile
from sentence_transformers import SentenceTransformer
from lib import pdf


async def embed(file: UploadFile):
    x = await pdf.read(file)
    sentence_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return sentence_embedding_model.encode([str(x)])[0], x


async def text_embed(text: str):
    sentence_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return sentence_embedding_model.encode([text])[0], text
