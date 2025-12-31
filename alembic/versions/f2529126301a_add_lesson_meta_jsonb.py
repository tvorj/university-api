"""add lesson meta jsonb

Revision ID: f2529126301a
Revises: 0eb3bed01833
Create Date: 2025-12-31 06:06:06.950051

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = 'f2529126301a'
down_revision = '0eb3bed01833'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("lesson", sa.Column("meta", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")))

def downgrade():
    op.drop_column("lesson", "meta")
