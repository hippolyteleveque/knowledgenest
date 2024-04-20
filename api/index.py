from fastapi import FastAPI
from api.auth.router import router as auth_router
from api.database import Base, engine

app = FastAPI()

app.include_router(auth_router, prefix="/api")


@app.get("/api")
async def root():
    return {"message": "Hello World"}


Base.metadata.create_all(engine)
