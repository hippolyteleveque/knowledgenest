from pinecone import Pinecone
from pinecone import ServerlessSpec
from fastapi import Depends
from pinecone.data.index import Index
from typing import Annotated
import time

from knowledgenest.config import config

PINECONE_API_KEY = config.PINECONE_API_KEY
PINECONE_INDEX_NAME = config.PINECONE_INDEX_NAME

EMBEDDING_MODEL_DIM = 1024
SIM_METRIC = "dotproduct"

idx: Index | None = None


def init_pinecone(
    api_key: str,
    idx_name: str,
    embd_dim: int,
    sim_metric: str,
) -> Index:
    """Setup pinecone index"""
    pc = Pinecone(api_key=api_key)
    spec = ServerlessSpec(cloud="gcp", region="europe-west4")
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if idx_name not in existing_indexes:
        pc.create_index(
            idx_name,
            dimension=embd_dim,
            metric=sim_metric,
            spec=spec,
        )
        while not pc.describe_index(idx_name).status["ready"]:
            time.sleep(1)

    return pc.Index(idx_name)


def get_vector_db():
    global idx
    if idx is None:
        # initialize pinecone
        idx = init_pinecone(
            PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL_DIM, SIM_METRIC
        )
    return idx


VectorDbSession = Annotated[Index, Depends(get_vector_db)]
