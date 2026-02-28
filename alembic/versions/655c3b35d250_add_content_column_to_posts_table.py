"""add content column to posts table

Revision ID: 655c3b35d250
Revises: c8663b85335b
Create Date: 2026-02-28 20:41:18.641253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '655c3b35d250'
down_revision: Union[str, Sequence[str], None] = 'c8663b85335b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
