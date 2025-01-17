import fastapi
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from huggingface_hub.hf_api import json
from lib import utils
from lib import vector, claysis, llm
from lib.claysis import qdrant_client
from utils.file import allowed_file
import numpy as np
from qdrant_client import QdrantClient, models
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/insert_doc")
async def insert_doc(file: UploadFile = File(...)):
    if not file.filename:
        return JSONResponse(status_code=400, content={"message": "No file uploaded"})
    if not await allowed_file(file.filename):
        return JSONResponse(
            status_code=400, content={"message": "Only PDF or TXT files are allowed."}
        )
    embedding, text = await vector.embed(file)

    insertion = claysis.insert_doc(str(text), file.filename, embedding.tolist())

    return insertion


@app.get("/vector_docs")
async def get_docs():
    print("docs")

    docs = qdrant_client.scroll(
        collection_name="docs",
        limit=100,
    )
    res = []
    print(docs)
    for doc in docs[0]:
        print("doc")
        print(doc)
        if "name" in doc.payload:
            res.append(doc.payload["name"])
        else:
            res.append(doc.id)
    return res


@app.post("/query")
async def query(query: str, context: str):
    if not query:
        return JSONResponse(status_code=400, content={"message": "No query provided"})

    retrieved_docs = await claysis.retrieve(query)
    res = [item.payload["text"] for item in retrieved_docs]

    response = llm.client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {
                "role": "user",
                "content": "Here is what you need to refer to",
            },
            *[
                {"role": "user", "content": item}
                for item in utils.split_strings_with_max_length(res)
            ],
            {
                "role": "user",
                "content": "this is the previous messages contextt --> " + context,
            },
            {
                "role": "user",
                "content": f"Now Heres The Question ,--> {query}, only respond based on the refrence, just give the answer no filler words, but formulate it in proper english like a conversation, if it doesnt exist in the refrence do not answer, keep your tone friendly and casual",
            },
        ],
        model="llama-3.1-8b-instant",
        temperature=0.6,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )
    answer = response.choices[0].message.content
    return answer


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
