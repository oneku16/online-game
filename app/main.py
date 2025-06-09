from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.player import player_router
from app.infrastructure.database import create_db_and_tables


@asynccontextmanager
async def startup(app_: FastAPI):
    yield await create_db_and_tables()


app = FastAPI(
    title="Online Game",
    description="API for creating online games as an event and play with other players.",
    version="1.0",
    contact={
        "name": "Elnazar Ulanbek uulu",
        "email": "elnazar.ulanbekuulu@outlook.com",
    },
    license_info={"name": "GNU License"},
    lifespan=startup
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(player_router)


@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Welcome to online-game"}
