from backend.routes import backend
from fastapi import FastAPI

app = FastAPI()

app.include_router(backend)
