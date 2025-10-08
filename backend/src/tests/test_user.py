import pytest
from fastapi import status
from src.db.models import UserDB


# ============ Тесты регистрации ============

@pytest.mark.asyncio
async def test_register_user(client, mocker):
    """Тест регистрации нового пользователя"""

    mocker.patch("src.db.crud._get_user_by_username", return_value=None)
    mocker.patch("src.core.security.Hasher.get_hash", return_value="hashed_password_mock")

    async def mock_add_user_func(user):
        user.id = 1
        return user

    mocker.patch("src.api.endpoints.users.add_user", side_effect=mock_add_user_func)

    response = await client.post("/users/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_register_user_already_exists(client, mocker):
    """Тест попытки регистрации существующего пользователя"""

    existing_user = UserDB(
        id=1,
        username="testuser",
        email="existing@example.com",
        password_hash="hashed"
    )

    mocker.patch("src.db.crud._get_user_by_username", return_value=existing_user)

    response = await client.post("/users/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    })

    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]


@pytest.mark.asyncio
async def test_register_user_invalid_email(client, mocker):
    """Тест регистрации с невалидным email"""

    mocker.patch("src.db.crud._get_user_by_username", return_value=None)

    response = await client.post("/users/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "invalid-email"
    })


    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ============ Тесты авторизации ============

@pytest.mark.asyncio
async def test_login_user_success(client, mocker):
    """Тест успешной авторизации пользователя"""

    mock_user = UserDB(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )

    mocker.patch("src.db.crud._get_user_by_username", return_value=mock_user)
    mocker.patch("src.core.security.Hasher.verify_password", return_value=True)

    response = await client.post("/users/login", json={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert len(data["access_token"]) > 0  # Просто проверяем, что токен не пустой


@pytest.mark.asyncio
async def test_login_user_wrong_password(client, mocker):
    """Тест авторизации с неправильным паролем"""

    mock_user = UserDB(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )

    mocker.patch("src.db.crud._get_user_by_username", return_value=mock_user)
    mocker.patch("src.core.security.Hasher.verify_password", return_value=False)

    response = await client.post("/users/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_user_not_found(client, mocker):
    """Тест авторизации несуществующего пользователя"""

    mocker.patch("src.db.crud._get_user_by_username", return_value=None)

    response = await client.post("/users/login", json={
        "username": "nonexistent",
        "password": "testpassword"
    })

    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]


@pytest.mark.asyncio
async def test_login_missing_credentials(client):
    """Тест авторизации без предоставления учётных данных"""

    response = await client.post("/users/login", json={})


    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
