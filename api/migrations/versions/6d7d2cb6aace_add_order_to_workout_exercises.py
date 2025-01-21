"""add_order_to_workout_exercises

Revision ID: 6d7d2cb6aace
Revises: 9a7c8e486e82
Create Date: 2024-03-26 18:38:46.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d7d2cb6aace'
down_revision: Union[str, None] = '9a7c8e486e82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add order column with default value 0
    op.add_column('workout_exercises', sa.Column('order', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Drop order column
    op.drop_column('workout_exercises', 'order')
