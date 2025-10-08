from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import session_manager
from src.db.models import TaskDB, UserDB


@session_manager
async def add_user(session: AsyncSession, user: UserDB):
    session.add(user)
    return user


async def _get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    return result.scalars().first()


@session_manager
async def get_user_by_id(session: AsyncSession, user_id: int):
    return await _get_user_by_id(session, user_id)


async def _get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(
        select(UserDB).where(UserDB.username == username)
    )
    return result.scalars().first()


@session_manager
async def get_user_by_username(session: AsyncSession, username: str):
    return await _get_user_by_username(session, username)

@session_manager
async def delete_user(session: AsyncSession, user_id: int):
    user = await _get_user_by_id(session, user_id)
    if user:
        await session.delete(user)


@session_manager
async def add_task(session: AsyncSession, task: TaskDB):
    session.add(task)
    return task

async def _get_tasks_by_user_id(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(TaskDB).where(TaskDB.user_id == user_id)
    )
    return result.scalars().all()


@session_manager
async def get_tasks_by_user_id(session: AsyncSession, user_id: int):
    return await _get_tasks_by_user_id(session, user_id)



@session_manager
async def delete_task(session: AsyncSession, user_id: int, task_id: int):
    result = await session.execute(
        select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    )
    task = result.scalars().first()
    if task:
        await session.delete(task)

@session_manager
async def update_task(
    session: AsyncSession, user_id: int, task_id: int, title: str, description: str | None = None
):
    result = await session.execute(
        select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    )
    task = result.scalars().first()

    if task:
        task.title = title
        task.description = description
        return task
    return None









