from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from langchain_community.document_loaders import YoutubeLoader
from langchain_mistralai import MistralAIEmbeddings
from starlette.status import HTTP_404_NOT_FOUND

from knowledgenest.videos.models import Video
from knowledgenest.videos.utils import extract_info_from_url
from knowledgenest.lib import MISTRAL_EMBEDDING_MODEL, MISTRALAI_API_KEY


def fetch_videos(user_id: str, db: Session, offset: int = 0, limit: int = 10):
    articles_count = db.query(Video).count()
    articles = (
        db.query(Video)
        .filter(Video.user_id == user_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return dict(articles_count=articles_count, articles=articles)


def delete_video_by_id(video_id: str, user_id: str, db: Session):
    article = (
        db.query(Video).filter(Video.id == video_id, Video.user_id == user_id).first()
    )
    if not article:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    db.delete(article)
    db.commit()
    return article


def process_new_video(url: str, user_id: str, db: Session):
    info = extract_info_from_url(url)
    new_video = Video(**info, url=url, user_id=user_id)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video


def embed_ang_ingest_video(video: Video, index):
    loader = YoutubeLoader.from_youtube_url(str(video.url), add_video_info=False)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    processed_docs = [process_doc(split, video, i) for i, split in enumerate(splits)]
    index.upsert(vectors=processed_docs)


def process_doc(doc, video: Video, i: int):
    embeddings = MistralAIEmbeddings(
        model=MISTRAL_EMBEDDING_MODEL, api_key=MISTRALAI_API_KEY
    )
    pc_obj = dict()
    pc_obj["metadata"] = dict(
        **doc.metadata,
        user_id=str(video.user_id),
        article_id=str(video.id),
        text=doc.page_content,
        type="video",
    )
    pc_obj["values"] = embeddings.embed_documents([doc.page_content])[0]
    pc_obj["id"] = f"{video.id}_{i}"
    return pc_obj


def delete_video_chunks_by_id(video_id: str, index):
    for ids in index.list(prefix=str(video_id)):
        index.delete(ids=ids)
    return True
