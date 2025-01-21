"""add missing columns to workout_exercises

Revision ID: 9a7c8e486e82
Revises: dfadd6043e50
Create Date: 2024-03-26 18:34:42.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a7c8e486e82'
down_revision = 'dfadd6043e50'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to workout_exercises table
    op.add_column('workout_exercises', sa.Column('sets', sa.Integer(), nullable=False, server_default='3'))
    op.add_column('workout_exercises', sa.Column('reps', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('workout_exercises', sa.Column('weight', sa.Float(), nullable=True))
    op.add_column('workout_exercises', sa.Column('notes', sa.String(length=500), nullable=True))


def downgrade():
    # Remove added columns
    op.drop_column('workout_exercises', 'notes')
    op.drop_column('workout_exercises', 'weight')
    op.drop_column('workout_exercises', 'reps')
    op.drop_column('workout_exercises', 'sets')
