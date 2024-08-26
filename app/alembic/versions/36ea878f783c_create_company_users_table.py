"""Create company_users table

Revision ID: 36ea878f783c
Revises: 04216a465596
Create Date: 2024-08-26 20:18:50.969187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36ea878f783c'
down_revision: Union[str, None] = '04216a465596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'company_users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('company_id', sa.UUID, nullable=False),
        sa.Column('user_id', sa.UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_company_users_company', 'company_users', 'companies', ['company_id'], ['id'])
    op.create_foreign_key('fk_company_users_user', 'company_users', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    op.drop_table('company_users')
