from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from database import get_db_context
from services import company as CompanyService
from services import auth as AuthService
from services.exception import AccessDeniedError, ResourceNotFoundError
from schemas.user import User
from models.company import CompanyModel, CompanyViewModel, SearchCompanyModel

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[CompanyViewModel])
async def get_all_companies(
    name: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
    if not user.is_admin:
        raise AccessDeniedError()

    conds = SearchCompanyModel(name, page, size)
    return CompanyService.get_companies(db, conds)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
async def create_company(
    request: CompanyModel, 
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
    ):
    if not user.is_admin:
        raise AccessDeniedError()

    return CompanyService.add_new_company(db, request)

@router.get("/{company_id}", response_model=CompanyViewModel)
async def get_company_detail(
    company_id: UUID,
    user: User = Depends(AuthService.token_interceptor),
    db: Session=Depends(get_db_context)
    ):
    if not user.is_admin:
            raise AccessDeniedError()
    
    company = CompanyService.get_company_by_id(db, company_id, joined_load=True)
    
    if company is None:
        raise ResourceNotFoundError()

    return company


@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def update_company(
    company_id: UUID,
    request: CompanyModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session=Depends(get_db_context),
    ):
    if not user.is_admin:
        raise AccessDeniedError()
    return CompanyService.update_company(db, company_id, request)