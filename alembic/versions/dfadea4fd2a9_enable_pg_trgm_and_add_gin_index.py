"""enable pg_trgm and add gin index

Revision ID: dfadea4fd2a9
Revises: f2529126301a
Create Date: 2025-12-31 06:08:09.338079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfadea4fd2a9'
down_revision = 'f2529126301a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.create_index(
        "ix_teacher_fio_trgm",
        "teacher",
        ["fio"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"fio": "gin_trgm_ops"},
    )

def downgrade():
    op.drop_index("ix_teacher_fio_trgm", table_name="teacher")
