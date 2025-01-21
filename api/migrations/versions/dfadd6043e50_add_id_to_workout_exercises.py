"""add_id_to_workout_exercises

Revision ID: dfadd6043e50
Revises: add_workout_exercises
Create Date: 2024-03-26 18:34:42.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfadd6043e50'
down_revision: Union[str, None] = 'add_workout_exercises'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing primary key constraint if any
    op.execute('ALTER TABLE workout_exercises DROP CONSTRAINT IF EXISTS workout_exercises_pkey')
    
    # Add id column
    op.execute('ALTER TABLE workout_exercises ADD COLUMN IF NOT EXISTS id SERIAL')
    
    # Set id values for existing rows
    op.execute('UPDATE workout_exercises SET id = DEFAULT')
    
    # Add primary key constraint
    op.execute('ALTER TABLE workout_exercises ADD PRIMARY KEY (id)')
    
    # Create index for better performance
    op.create_index(op.f('ix_workout_exercises_id'), 'workout_exercises', ['id'], unique=True)


def downgrade() -> None:
    # Remove index first
    op.drop_index(op.f('ix_workout_exercises_id'), table_name='workout_exercises')
    
    # Remove primary key constraint and id column
    op.execute('ALTER TABLE workout_exercises DROP CONSTRAINT workout_exercises_pkey')
    op.execute('ALTER TABLE workout_exercises DROP COLUMN id')
