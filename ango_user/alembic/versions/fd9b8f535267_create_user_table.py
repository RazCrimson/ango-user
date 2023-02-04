"""create user table

Revision ID: fd9b8f535267
Revises: 
Create Date: 2023-02-04 22:34:13.187254

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'fd9b8f535267'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("pass_hash", sa.LargeBinary, nullable=False),
        sa.Column("init_vector", sa.LargeBinary, nullable=False),
        sa.Column("last_signed_in", sa.types.TIMESTAMP, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("user")