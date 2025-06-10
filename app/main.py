from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.tournament_api import tournament_router
from .infrastructure.database import create_db_and_tables


@asynccontextmanager
async def startup(app_: FastAPI) -> AsyncGenerator[Any]:
    yield await create_db_and_tables()  # type: ignore [func-returns-value]


app = FastAPI(
    title="Online Game",
    description="API for creating online games as an event and play with other players.",
    version="1.0",
    contact={
        "name": "Elnazar Ulanbek uulu",
        "email": "elnazar.ulanbekuulu@outlook.com",
    },
    license_info={"name": "GNU License"},
    lifespan=startup,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=tournament_router)


@app.get("/", tags=["Health Check"])
async def root() -> dict[str, str]:
    return {"message": "Welcome to online-game"}
