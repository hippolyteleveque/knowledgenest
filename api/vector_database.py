from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import time
import os

load_dotenv(dotenv_path="api.env")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "knowledgenest"
EMBEDDING_MODEL_DIM = 1536
SIM_METRIC = "dotproduct"

pc = Pinecone(api_key=PINECONE_API_KEY)

spec = ServerlessSpec(cloud="aws", region="eu-west-1")

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
