import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime
from src.db.models import UserDB


@pytest_asyncio.fixture
async def client():
    """HTTP клиент для тестирования FastAPI приложения"""
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


    app.dependency_overrides.clear()


@pytest_asyncio.fixture
def mock_user():
    """Мок пользователя для тестов"""
    return UserDB(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )


@pytest_asyncio.fixture
def authenticated_client(client, mock_user):
    """Клиент с авторизованным пользователем"""
    from src.main import app
    from src.core.security import get_current_user

    app.dependency_overrides[get_current_user] = lambda: mock_user

    return client
