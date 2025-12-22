"""use_utc_time

Revision ID: 35e5c4e5a2a5
Revises: e67a5f074b34
Create Date: 2025-10-27 12:40:44.749508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '35e5c4e5a2a5'
down_revision = 'e67a5f074b34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Convert all datetime fields to UTC-aware timestamps."""
    # Articles table
    op.alter_column(
        'articles', 'created_at',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )
    op.alter_column(
        'articles', 'updated_at',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )

    # Comments table
    op.alter_column(
        'comments', 'created_at',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )
    op.alter_column(
        'comments', 'updated_at',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )

    # Users table
    op.alter_column(
        'users', 'deleted_at',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )


def downgrade() -> None:
    """Revert datetime fields back to naive timestamps."""
    # Articles table
    op.alter_column(
        'articles', 'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )
    op.alter_column(
        'articles', 'updated_at',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )

    # Comments table
    op.alter_column(
        'comments', 'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )
    op.alter_column(
        'comments', 'updated_at',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )

    # Users table
    op.alter_column(
        'users', 'deleted_at',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )
