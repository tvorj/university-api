"""add gin index on lesson meta

Revision ID: 85812451d911
Revises: dfadea4fd2a9
Create Date: 2025-12-31 06:12:28.923593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85812451d911'
down_revision = 'dfadea4fd2a9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_lesson_meta_gin",
        "lesson",
        ["meta"],
        unique=False,
        postgresql_using="gin",
    )

def downgrade():
    op.drop_index("ix_lesson_meta_gin", table_name="lesson")
