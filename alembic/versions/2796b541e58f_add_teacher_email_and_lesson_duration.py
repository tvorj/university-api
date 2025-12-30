"""add teacher email and lesson duration

Revision ID: 2796b541e58f
Revises: 14279023c115
Create Date: 2025-12-30 17:22:25.238653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2796b541e58f'
down_revision = '14279023c115'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("teacher", sa.Column("email", sa.Text(), nullable=True))
    op.create_unique_constraint("uq_teacher_email", "teacher", ["email"])
    op.add_column("lesson", sa.Column("duration_min", sa.Integer(), nullable=True))

def downgrade():
    op.drop_column("lesson", "duration_min")
    op.drop_constraint("uq_teacher_email", "teacher", type_="unique")
    op.drop_column("teacher", "email")
