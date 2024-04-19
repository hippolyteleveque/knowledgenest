from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="api.env")

pg_host = os.getenv("POSTGRES_HOST")
pg_user = os.getenv("POSTGRES_USER")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DATABASE")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+pg8000://{pg_user}:{pg_password}@{pg_host}/{pg_db}"
)

# SQLALCHEMY_DATABASE_URL = "postgresql://root:secret@localhost:5432/knowledgenest"
# SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://default:7uDUGB4PHeTR@ep-proud-union-a2x1hvx7-pooler.eu-central-1.aws.neon.tech:5432/verceldb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
