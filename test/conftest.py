import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.dependecies.services import get_tournament_service
from app.errors.tournament_errors import PlayerAlreadyRegisteredError
from app.infrastructure.database import Base, get_db
from app.main import app
from app.schemas import TournamentRead

test_engine = create_async_engine(settings.database_settings.test_url, echo=False)
TestSessionLocal = async_sessionmaker(test_engine,  expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(prepare_test_db) -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncClient:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()