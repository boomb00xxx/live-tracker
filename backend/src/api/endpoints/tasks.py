from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas.task import AddTask, EditTask, ReadTask
from src.core.security import get_current_user
from src.db.crud import add_task, delete_task, get_tasks_by_user_id, update_task
from src.db.models import TaskDB

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/user/{user_id}")
async def create_task(user_id: int, data: AddTask, user=Depends(get_current_user)) -> ReadTask:
    """Создать задачу для пользователя."""
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    task = TaskDB(
        title=data.title,
        description=data.description,
        user_id=user_id
    )
    new_task = await add_task(task)
    return new_task


@router.get("/user/{user_id}")
async def get_tasks(user_id: int, user=Depends(get_current_user)) -> List[ReadTask]:
    """Получить все задачи пользователя."""
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    tasks = await get_tasks_by_user_id(user_id)
    return tasks


@router.put("/user/{user_id}/task/{task_id}")
async def edit_task(user_id: int, task_id: int, data: EditTask, user=Depends(get_current_user)) -> ReadTask:
    """Обновить задачу по ID."""
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    task = await update_task(user_id, task_id, data.title)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if data.description:
        task.description = data.description
    return task


@router.delete("/user/{user_id}/task/{task_id}")
async def remove_task(user_id: int, task_id: int, user=Depends(get_current_user)):
    """Удалить задачу пользователя."""
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    await delete_task(user_id, task_id)
    return {"detail": "Задача удалена"}



