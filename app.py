from src.backend.routes import users, teams, scores, stages
from src.backend.auth import auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.dependencies import engine
from sqlmodel import SQLModel

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000"
    "http://localhost:80",
    "http://10.128.0.6:3000",
    "http://10.128.0.6:80",
    "http://10.128.0.6",
    "http://51.250.1.125",
    "http://51.250.1.125:3000",
    "http://51.250.1.125:80",
    "https://51.250.1.125",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# version 1
app.include_router(auth, prefix="/api/v1", tags=["Auth"])
app.include_router(users, prefix="/api/v1", tags=["User"])
app.include_router(teams, prefix="/api/v1", tags=["Team"])
app.include_router(scores, prefix="/api/v1", tags=["Score"])
app.include_router(stages, prefix="/api/v1", tags=["Stage"])
