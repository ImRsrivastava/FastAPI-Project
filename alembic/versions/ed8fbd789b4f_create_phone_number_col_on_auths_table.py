"""create phone number col on auths table

Revision ID: ed8fbd789b4f
Revises: 
Create Date: 2026-02-01 20:59:02.848607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed8fbd789b4f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('auths', sa.Column('phone_number', sa.String(15), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('auths', 'phone_number')
