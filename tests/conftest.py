import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import asyncio
from app.core.database import engine


@pytest.fixture(scope="session", autouse=True)
def cleanup_db_engine():
    yield
    # Properly close async engine at end of test session
    loop = asyncio.new_event_loop()
    loop.run_until_complete(engine.dispose())
    loop.close()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac
