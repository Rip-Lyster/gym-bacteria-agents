"""Add workout_exercises table

Revision ID: add_workout_exercises
Revises: 445b9f944bc5
Create Date: 2024-01-21 02:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_workout_exercises'
down_revision: Union[str, None] = '445b9f944bc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workout_exercises table
    op.create_table('workout_exercises',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workout_id', sa.Integer(), nullable=False),
        sa.Column('exercise_type_id', sa.Integer(), nullable=False),
        sa.Column('sets', sa.Integer(), nullable=False),
        sa.Column('reps', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['exercise_type_id'], ['exercise_types.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # Add index for faster lookups
    op.create_index('idx_workout_exercises_workout_id', 'workout_exercises', ['workout_id'])
    op.create_index('idx_workout_exercises_exercise_type_id', 'workout_exercises', ['exercise_type_id'])
    op.create_index('idx_workout_exercises_order', 'workout_exercises', ['workout_id', 'order'])


def downgrade() -> None:
    op.drop_index('idx_workout_exercises_order')
    op.drop_index('idx_workout_exercises_exercise_type_id')
    op.drop_index('idx_workout_exercises_workout_id')
    op.drop_table('workout_exercises') 