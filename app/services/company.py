from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from schemas.company import Company
from models.company import CompanyModel, SearchCompanyModel
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError


def get_companies(db: Session, conds: SearchCompanyModel) -> List[Company]:
    # Default of joinedload is LEFT OUTER JOIN
    query = select(Company).options(
        joinedload(Company.tasks, innerjoin=True),
        joinedload(Company.users, innerjoin=True))
    
    if conds.name is not None:
        query = query.filter(Company.name.like(f"%{conds.name}%"))
    
    query = query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).unique().fetchall()


def get_company_by_id(db: Session, id: UUID, /, joined_load = False) -> Company:
    query = select(Company).filter(Company.id == id)
    
    if joined_load:
        query.options(
            joinedload(Company.tasks, innerjoin=True),
            joinedload(Company.users))
    
    return db.scalars(query).first()


def add_new_company(db: Session, data: CompanyModel) -> Company:
    company = Company(**data.model_dump())
    company.created_at = get_current_utc_time()
    company.updated_at = get_current_utc_time()

    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company


def update_company(db: Session, id: UUID, data: CompanyModel) -> Company:
    company = get_company_by_id(db, id)

    if company is None:
        raise ResourceNotFoundError()

    company.name = data.name
    company.description = data.description
    company.rating = data.rating
    company.updated_at = get_current_utc_time()
    
    db.commit()
    db.refresh(company)
    
    return company
