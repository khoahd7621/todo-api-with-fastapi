"""Generate seed data

Revision ID: 14382942a71e
Revises: 73345c75a495
Create Date: 2024-08-26 20:59:26.628214

"""
from typing import Sequence, Union

from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
from sqlalchemy import Table, MetaData

from schemas.task import ETaskStatus, EPriority
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision: str = '14382942a71e'
down_revision: Union[str, None] = '73345c75a495'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    companyid_1 = uuid4()
    companyid_2 = uuid4()
    user_id_1 = uuid4()
    user_id_2 = uuid4()
    task_id_1 = uuid4()
    task_id_2 = uuid4()
    task_id_3 = uuid4()
    task_id_4 = uuid4()
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    meta = MetaData()

    companies = Table('companies', meta, autoload_with=op.get_bind())
    users = Table('users', meta, autoload_with=op.get_bind())
    tasks = Table('tasks', meta, autoload_with=op.get_bind())

    op.bulk_insert(
        companies,
        [
            {
                'id': companyid_1,
                'name': 'Company 1',
                'description': 'Company 1 description',
                'rating': 0,
                'created_at': created_at,
                'updated_at': updated_at
            },
            {
                'id': companyid_2,
                'name': 'Company 2',
                'description': 'Company 2 description',
                'rating': 0,
                'created_at': created_at,
                'updated_at': updated_at
            }
        ]
    )

    op.bulk_insert(
        users,
        [
            {
                'id': user_id_1,
                'email': 'admin@admin.com',
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': '1',
                'hashed_password': get_password_hash(ADMIN_DEFAULT_PASSWORD),
                'is_active': True,
                'is_admin': True,
                'created_at': created_at,
                'updated_at': updated_at,
                'company_id': companyid_1
            },
            {
                'id': user_id_2,
                'email': 'user@user.com',
                'username': 'user',
                'first_name': 'User',
                'last_name': '1',
                'hashed_password': get_password_hash(ADMIN_DEFAULT_PASSWORD),
                'is_active': True,
                'is_admin': False,
                'created_at': created_at,
                'updated_at': updated_at,
                'company_id': companyid_2
            }
        ]
    )

    op.bulk_insert(
        tasks,
        [
            {
                'id': task_id_1,
                'summary': 'Task 1',
                'description': 'Task 1 description',
                'status': ETaskStatus.IN_PROGRESS.name,
                'priority': EPriority.HIGH.name,
                'company_id': companyid_1,
                'user_id': user_id_1,
                'created_at': created_at,
                'updated_at': updated_at
            },
            {
                'id': task_id_2,
                'summary': 'Task 2',
                'description': 'Task 2 description',
                'status': ETaskStatus.TODO.name,
                'priority': EPriority.LOW.name,
                'company_id': companyid_2,
                'user_id': user_id_1,
                'created_at': created_at,
                'updated_at': updated_at
            },
            {
                'id': task_id_3,
                'summary': 'Task 3',
                'description': 'Task 3 description',
                'status': ETaskStatus.DONE.name,
                'priority': EPriority.MEDIUM.name,
                'company_id': companyid_1,
                'user_id': user_id_2,
                'created_at': created_at,
                'updated_at': updated_at
            },
            {
                'id': task_id_4,
                'summary': 'Task 4',
                'description': 'Task 4 description',
                'status': ETaskStatus.TODO.name,
                'priority': EPriority.MEDIUM.name,
                'company_id': companyid_2,
                'user_id': user_id_2,
                'created_at': created_at,
                'updated_at': updated_at
            },
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM company_users")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM companies")
    op.execute("DELETE FROM tasks")
