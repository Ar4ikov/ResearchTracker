from src.backend.routes import users, teams, scores
from fastapi import FastAPI
from src.backend.dependencies import engine
from sqlmodel import SQLModel

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# version 1
app.include_router(users, prefix="/api/v1", tags=["User"])
app.include_router(teams, prefix="/api/v1", tags=["Team"])
app.include_router(scores, prefix="/api/v1", tags=["Score"])
