from pinecone import Pinecone
from pinecone import ServerlessSpec
from fastapi import Depends
from pinecone.data.index import Index
from typing import Annotated
import time
import os


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "knowledgenest"
EMBEDDING_MODEL_DIM = 1024
SIM_METRIC = "dotproduct"

pc = Pinecone(api_key=PINECONE_API_KEY)

spec = ServerlessSpec(cloud="aws", region="us-east-1")

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

# check if index already exists (it shouldn't if this is first time)
if INDEX_NAME not in existing_indexes:
    # if does not exist, create index
    pc.create_index(
        INDEX_NAME,
        dimension=EMBEDDING_MODEL_DIM,  # dimensionality of ada 002
        metric=SIM_METRIC,
        spec=spec,
    )
    # wait for index to be initialized
    while not pc.describe_index(INDEX_NAME).status["ready"]:
        time.sleep(1)


# connect to index
def get_vector_db():
    # maybe not ideal
    index = pc.Index(INDEX_NAME)
    try:
        yield index
    finally:
        pass


VectorDbSession = Annotated[Index, Depends(get_vector_db)]
