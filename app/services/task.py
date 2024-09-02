from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models.task import TaskCreateModel, SearchTaskModel, TaskUpdateModel, TaskUpdateStatusModel
from schemas.task import Task, ETaskStatus
from schemas.user import User
from schemas.company import Company
from services.exception import AccessDeniedError, ResourceNotFoundError, BadRequestError


async def get_tasks(
    async_db: AsyncSession,
    conditions: SearchTaskModel) -> list[Task]:
    
    query = select(Task).order_by(Task.created_at)
    
    if conditions.company_id is not None:
        utils.validate_uuid(conditions.company_id)
        query = query.filter(Task.company_id == conditions.company_id)
    
    if conditions.user_id is not None:
        utils.validate_uuid(conditions.user_id)
        query = query.filter(Task.user_id == conditions.user_id)
    
    result = await async_db.scalars(query)
    return result.all()


def get_my_tasks(db: Session, user_id: UUID) -> list[Task]:
    return db.scalars(select(Task).filter(Task.user_id == user_id)).all()


def get_task_by_id(db: Session, task_id: UUID) -> Task:
    return db.scalars(select(Task).filter(Task.id == task_id)).first()


def add_new_task(db: Session, data: TaskCreateModel) -> Task:
    if data.user_id is not None:
        user = db.scalars(select(User).filter(User.id == data.user_id)).first()

        if user is None:
            raise BadRequestError(msg="User not found")

        if user.company_id != data.company_id:
            raise BadRequestError(msg="User is not in this company")
    else:
        company = db.scalars(select(Company).filter(Company.id == data.company_id)).first()

        if company is None:
            raise BadRequestError(msg="Company not found")


    task = Task(**data.model_dump())

    task.status = ETaskStatus.TODO

    task.created_at = utils.get_current_utc_time()
    task.updated_at = utils.get_current_utc_time()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


def update_task(db: Session, id: UUID, data: TaskUpdateModel, user: User) -> Task:
    task = get_task_by_id(db, id)
    if task is None:
        raise ResourceNotFoundError()
    
    if user.is_admin is False:
        if (task.user_id is None or task.user_id != user.id):
            raise AccessDeniedError()
        if (data.company_id is not None or data.user_id is not None):
            raise BadRequestError(msg="You can not update company or user id")
    else:
        if (data.company_id is not None and data.user_id is None) or (data.company_id is None and data.user_id is not None):
            raise BadRequestError(msg="You must update both company and user id")
        user = db.scalars(select(User).filter(User.id == data.user_id)).first()
        if user is None:
            raise BadRequestError(msg="User not found")
        if user.company_id != data.company_id:
            raise BadRequestError(msg="User is not in this company")
        task.user_id = data.user_id
        task.company_id = data.company_id
    
    task.summary = data.summary
    task.description = data.description
    task.priority = data.priority
    
    task.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    return task


def update_task_status(db: Session, id: UUID, data: TaskUpdateStatusModel, user: User) -> Task:
    task = get_task_by_id(db, id)
    if task is None:
        raise ResourceNotFoundError()
    
    if user.is_admin is False and (task.user_id is None or task.user_id != user.id):
        raise AccessDeniedError()
    
    task.status = data.status
    task.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, id: UUID) -> None:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()
    
    if task.user_id is not None:
        raise AccessDeniedError()
    
    db.delete(task)
    db.commit()
