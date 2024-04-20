from fastapi import FastAPI
from api.auth.router import router as auth_router
from api.articles.router import router as articles_router
from api.database import Base, engine

app = FastAPI(root_path="/api")

app.include_router(auth_router)
app.include_router(articles_router)


@app.get("/api")
async def root():
    return {"message": "Hello World"}


Base.metadata.create_all(engine)
