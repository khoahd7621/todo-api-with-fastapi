"""Create users table

Revision ID: 04216a465596
Revises: 618cb712086f
Create Date: 2024-08-26 20:16:23.230801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04216a465596'
down_revision: Union[str, None] = '618cb712086f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_admin', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('company_id', sa.UUID, nullable=False),
    )
    op.create_index('idx_usr_email', 'users', ['email'])
    op.create_index('idx_usr_username', 'users', ['username'])
    op.create_index('idx_usr_name', 'users', ['first_name', 'last_name'])
    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])


def downgrade() -> None:
    op.drop_table('users')
