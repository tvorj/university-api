"""add lesson indexes

Revision ID: 0eb3bed01833
Revises: 2796b541e58f
Create Date: 2025-12-30 17:31:15.818751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eb3bed01833'
down_revision = '2796b541e58f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_lesson_data", "lesson", ["data"])
    op.create_index("ix_lesson_gruppa", "lesson", ["gruppa"])
    op.create_index("ix_lesson_teacher_data", "lesson", ["teacher_id", "data"])

def downgrade():
    op.drop_index("ix_lesson_teacher_data", table_name="lesson")
    op.drop_index("ix_lesson_gruppa", table_name="lesson")
    op.drop_index("ix_lesson_data", table_name="lesson")
