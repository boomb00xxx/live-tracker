import pytest
from fastapi import status
from src.db.models import TaskDB
from datetime import datetime


# ============ Тесты создания тасок ============

@pytest.mark.asyncio
async def test_create_task(authenticated_client, mock_user, mocker):
    """Тест создания таски"""

    async def mock_add_task_func(task):
        task.id = 1
        task.created_at = datetime.now()
        return task

    mocker.patch("src.api.endpoints.tasks.add_task", side_effect=mock_add_task_func)

    response = await authenticated_client.post(
        f"/tasks/user/{mock_user.id}",
        json={"title": "Test Task", "description": "Test Description"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"


@pytest.mark.asyncio
async def test_create_task_forbidden(authenticated_client, mock_user):
    """Тест создания таски для другого пользователя (403 Forbidden)"""

    other_user_id = mock_user.id + 1

    response = await authenticated_client.post(
        f"/tasks/user/{other_user_id}",
        json={"title": "Test Task", "description": "Test Description"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_task_unauthorized(client):
    """Тест создания таски без авторизации"""

    response = await client.post(
        "/tasks/user/1",
        json={"title": "Test Task", "description": "Test Description"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============ Тесты получения тасок ============

@pytest.mark.asyncio
async def test_get_user_tasks(authenticated_client, mock_user, mocker):
    """Тест получения списка тасок пользователя"""

    mock_tasks = [
        TaskDB(
            id=1,
            title="Task 1",
            description="Description 1",
            user_id=mock_user.id,
            created_at=datetime.now()
        ),
        TaskDB(
            id=2,
            title="Task 2",
            description="Description 2",
            user_id=mock_user.id,
            created_at=datetime.now()
        )
    ]
    mocker.patch("src.db.crud._get_tasks_by_user_id", return_value=mock_tasks)

    response = await authenticated_client.get(f"/tasks/user/{mock_user.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


@pytest.mark.asyncio
async def test_get_user_tasks_empty(authenticated_client, mock_user, mocker):
    """Тест получения пустого списка тасок"""

    mocker.patch("src.db.crud._get_tasks_by_user_id", return_value=[])

    response = await authenticated_client.get(f"/tasks/user/{mock_user.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_tasks_forbidden(authenticated_client, mock_user):
    """Тест попытки получить таски другого пользователя"""

    other_user_id = mock_user.id + 1

    response = await authenticated_client.get(f"/tasks/user/{other_user_id}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_tasks_unauthorized(client):
    """Тест получения тасок без авторизации"""

    response = await client.get("/tasks/user/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============ Тесты обновления тасок ============

@pytest.mark.asyncio
async def test_update_task(authenticated_client, mock_user, mocker):
    """Тест обновления таски"""

    updated_task = TaskDB(
        id=1,
        title="Updated Task",
        description="Old Description",
        user_id=mock_user.id,
        created_at=datetime.now()
    )

    async def mock_update_task_func(user_id, task_id, title):
        updated_task.title = title
        return updated_task

    mocker.patch("src.api.endpoints.tasks.update_task", side_effect=mock_update_task_func)

    response = await authenticated_client.put(
        f"/tasks/user/{mock_user.id}/task/1",
        json={"title": "Updated Task", "description": "Updated Description"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Task"


@pytest.mark.asyncio
async def test_update_task_not_found(authenticated_client, mock_user, mocker):
    """Тест обновления несуществующей таски"""

    mocker.patch("src.api.endpoints.tasks.update_task", return_value=None)

    response = await authenticated_client.put(
        f"/tasks/user/{mock_user.id}/task/999",
        json={"title": "Updated Task", "description": "Updated Description"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_task_forbidden(authenticated_client, mock_user):
    """Тест попытки обновить таску другого пользователя"""

    other_user_id = mock_user.id + 1

    response = await authenticated_client.put(
        f"/tasks/user/{other_user_id}/task/1",
        json={"title": "Updated Task", "description": "Updated Description"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_task_unauthorized(client):
    """Тест обновления таски без авторизации"""

    response = await client.put(
        "/tasks/user/1/task/1",
        json={"title": "Updated Task", "description": "Updated Description"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============ Тесты удаления тасок ============

@pytest.mark.asyncio
async def test_delete_task(authenticated_client, mock_user, mocker):
    """Тест удаления таски"""

    mocker.patch("src.api.endpoints.tasks.delete_task", return_value=None)

    response = await authenticated_client.delete(f"/tasks/user/{mock_user.id}/task/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Задача удалена"}


@pytest.mark.asyncio
async def test_delete_task_forbidden(authenticated_client, mock_user):
    """Тест попытки удалить таску другого пользователя"""

    other_user_id = mock_user.id + 1

    response = await authenticated_client.delete(f"/tasks/user/{other_user_id}/task/1")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_task_unauthorized(client):
    """Тест удаления таски без авторизации"""

    response = await client.delete("/tasks/user/1/task/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
