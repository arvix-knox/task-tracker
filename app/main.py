from fastapi import FastAPI
from app.api.v1.routers import auth

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def start():
    return {"status": "ok"}

