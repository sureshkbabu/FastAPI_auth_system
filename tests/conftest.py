import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest
from app.core.database import engine


@pytest.fixture(scope="session", autouse=True)
async def cleanup_db_engine():
    yield
    await engine.dispose()

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac
