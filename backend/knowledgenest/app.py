from fastapi import FastAPI, Response
from knowledgenest.auth.router import router as auth_router
from knowledgenest.articles.router import router as articles_router
from knowledgenest.chat.router import router as chat_router
from knowledgenest.videos.router import router as videos_router
from starlette.status import HTTP_200_OK

app = FastAPI(root_path="/api/v1")

app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(chat_router)
app.include_router(videos_router)


@app.get("/health")
def health():
    return Response(status_code=HTTP_200_OK)
