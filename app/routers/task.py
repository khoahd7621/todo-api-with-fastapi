from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.task import TaskCreateModel, TaskViewModel, SearchTaskModel, TaskUpdateModel, TaskUpdateStatusModel
from services.exception import AccessDeniedError, ResourceNotFoundError
from services import task as TaskService
from schemas.user import User
from services import auth as AuthService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskViewModel])
async def get_all_tasks(
    company_id: str = Query(default=None),
    user_id: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    user: User = Depends(AuthService.token_interceptor),
    async_db: AsyncSession = Depends(get_async_db_context)):
    if not user.is_admin:
        raise AccessDeniedError()
    conditions = SearchTaskModel(company_id, user_id, page, size)
    return await TaskService.get_tasks(async_db, conditions)

@router.get("/me", status_code=status.HTTP_200_OK, response_model=list[TaskViewModel])
async def get_my_tasks(
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context)):
    return TaskService.get_my_tasks(db, user.id)

@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def get_task_by_id(
    task_id: UUID, 
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context)):    
    task = TaskService.get_task_by_id(db, task_id)

    if task is None:
        raise ResourceNotFoundError()
    
    if user.is_admin is False and (task.user_id is None or task.user_id != user.id):
        raise AccessDeniedError()

    return task


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskCreateModel, 
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context)):
    if not user.is_admin:
        raise AccessDeniedError()
    return TaskService.add_new_task(db, request)


# Update task status
@router.patch("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task_status(
    task_id: UUID,
    request: TaskUpdateStatusModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
    ):
    return TaskService.update_task_status(db, task_id, request, user)


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    task_id: UUID,
    request: TaskUpdateModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
    ):
    return TaskService.update_task(db, task_id, request, user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: Session = Depends(get_db_context)):
    TaskService.delete_task(db, task_id)