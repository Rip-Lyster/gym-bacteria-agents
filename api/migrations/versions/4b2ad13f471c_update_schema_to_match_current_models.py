"""update schema to match current models

Revision ID: 4b2ad13f471c
Revises: 6d7d2cb6aace
Create Date: 2025-01-25 19:42:07.389127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4b2ad13f471c'
down_revision: Union[str, None] = '6d7d2cb6aace'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop all existing data first
    op.drop_table('workout_exercises')
    op.drop_table('workouts')
    op.drop_table('training_blocks')
    op.drop_table('training_plans')
    op.drop_table('exercise_types')
    op.drop_table('users')
    
    # Create tables with new schema
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('access_key', sa.String(length=64), nullable=False),
        sa.Column('nickname', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_access', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('access_key')
    )
    
    op.create_table('exercise_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('training_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('progression_type', sa.String(length=50), nullable=True),
        sa.Column('target_weekly_hours', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('training_blocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('primary_focus', sa.String(length=50), nullable=False),
        sa.Column('duration_weeks', sa.Integer(), nullable=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['training_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('workouts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('block_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('planned_date', sa.Date(), nullable=False),
        sa.Column('actual_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('exercises', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['block_id'], ['training_blocks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table('workouts')
    op.drop_table('training_blocks')
    op.drop_table('training_plans')
    op.drop_table('exercise_types')
    op.drop_table('users')
