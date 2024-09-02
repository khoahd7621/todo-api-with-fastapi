"""Create tasks table

Revision ID: 73345c75a495
Revises: 36ea878f783c
Create Date: 2024-08-26 20:27:28.261301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas.task import ETaskStatus, EPriority


# revision identifiers, used by Alembic.
revision: str = '73345c75a495'
down_revision: Union[str, None] = '04216a465596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('summary', sa.String(255), nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status', sa.Enum(ETaskStatus), nullable=False, default=ETaskStatus.TODO),
        sa.Column('priority', sa.Enum(EPriority), nullable=False, default=EPriority.LOW),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('company_id', sa.UUID, nullable=False),
        sa.Column('user_id', sa.UUID, nullable=False)
    )
    op.create_index('idx_task_summary', 'tasks', ['summary'])
    op.create_foreign_key('fk_task_owner', 'tasks', 'companies', ['company_id'], ['id'])
    op.create_foreign_key('fk_task_assignee', 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table('tasks')
    op.execute("DROP TYPE IF EXISTS task_status")
    op.execute("DROP TYPE IF EXISTS priority")
