from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from knowledgenest.articles.models import Article
from knowledgenest.articles.utils import (
    convert_properties_to_fields,
    extract_meta_properties,
)
from starlette.status import HTTP_404_NOT_FOUND
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-ada-002"


def process_new_article(url: str, user_id: str, db: Session):
    # First version, we only create the article in base,
    properties = extract_meta_properties(url)
    fields = convert_properties_to_fields(properties)
    new_article = Article(**fields, user_id=user_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def fetch_articles(user_id: str, db: Session, offset: int = 0, limit: int = 10):
    articles_count = db.query(Article).count()
    articles = (
        db.query(Article)
        .filter(Article.user_id == user_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return dict(articles_count=articles_count, articles=articles)


def delete_article_by_id(article_id: str, user_id: str, db: Session):
    article = (
        db.query(Article)
        .filter(Article.id == article_id, Article.user_id == user_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    db.delete(article)
    db.commit()
    return article


def embed_and_ingest_article(article: Article, index):
    url = article.url
    loader = WebBaseLoader(
        web_paths=(str(url),),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    processed_docs = [process_doc(split, article, i) for i, split in enumerate(splits)]
    index.upsert(vectors=processed_docs)


def process_doc(doc, article: Article, i: int):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    pc_obj = dict()
    pc_obj["metadata"] = dict(
        **doc.metadata,
        user_id=article.user_id,
        article_id=article.id,
        text=doc.page_content,
    )
    pc_obj["values"] = embeddings.embed_documents([doc.page_content])[0]
    pc_obj["id"] = f"{article.id}_{i}"
    return pc_obj


def delete_article_chunks_by_id(article_id: str, index):
    for ids in index.list(prefix=str(article_id)):
        index.delete(ids=ids)
    return True
