from pinecone import Pinecone
from pinecone import ServerlessSpec
from fastapi import Depends
from pinecone.data.index import Index
from typing import Annotated
import time

from knowledgenest.config import config

PINECONE_API_KEY = config["PINECONE_API_KEY"]
PINECONE_INDEX_NAME = config["PINECONE_INDEX_NAME"]

EMBEDDING_MODEL_DIM = 1024
SIM_METRIC = "dotproduct"

pc = None


def initialize_pinecone():
    global pc
    if pc is None:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        spec = ServerlessSpec(cloud="gcp", region="europe-west4")
        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

        if PINECONE_INDEX_NAME not in existing_indexes:
            pc.create_index(
                PINECONE_INDEX_NAME,
                dimension=EMBEDDING_MODEL_DIM,
                metric=SIM_METRIC,
                spec=spec,
            )
            while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
                time.sleep(1)


def get_vector_db():
    initialize_pinecone()
    return pc.Index(PINECONE_INDEX_NAME)


VectorDbSession = Annotated[Index, Depends(get_vector_db)]
