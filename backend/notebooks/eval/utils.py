from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.document_loaders import YoutubeLoader

MISTRAL_EMBEDDING_MODEL = "mistral-embed"

def embed_and_ingest_article(url, index):
    loader = WebBaseLoader(
        web_paths=(str(url),),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    processed_docs = [process_article_doc(url, split, i) for i, split in enumerate(splits)]
    index.upsert(vectors=processed_docs)


def process_article_doc(url, doc, i: int):
    embeddings = MistralAIEmbeddings(model=MISTRAL_EMBEDDING_MODEL)
    pc_obj = dict()
    pc_obj["metadata"] = dict(
        **doc.metadata,
        text=doc.page_content,
        content_id=url,
        type="article",
    )
    pc_obj["values"] = embeddings.embed_documents([doc.page_content])[0]
    pc_obj["id"] = f"{url}_{i}"
    return pc_obj

def embed_and_ingest_video(url: str, index):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    processed_docs = [process_video_doc(url, split, i) for i, split in enumerate(splits)]
    index.upsert(vectors=processed_docs)


def process_video_doc(url, doc, i: int):
    embeddings = MistralAIEmbeddings(
        model=MISTRAL_EMBEDDING_MODEL,
    )
    pc_obj = dict()
    pc_obj["metadata"] = dict(
        **doc.metadata,
        content_id=url,
        text=doc.page_content,
        type="video",
    )
    pc_obj["values"] = embeddings.embed_documents([doc.page_content])[0]
    pc_obj["id"] = f"{url}_{i}"
    return pc_obj


