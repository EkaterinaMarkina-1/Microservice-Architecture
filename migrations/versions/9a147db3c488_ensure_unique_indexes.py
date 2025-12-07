"""ensure_unique_indexes

Revision ID: 9a147db3c488
Revises: 35e5c4e5a2a5
Create Date: 2025-10-27 12:59:37.414356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '9a147db3c488'
down_revision: Union[str, Sequence[str], None] = '35e5c4e5a2a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавляем уникальные индексы, если их ещё нет."""
    conn = op.get_bind()
    inspector = inspect(conn)

    # User.email
    if 'ix_users_email' not in [idx['name'] for idx in inspector.get_indexes('users')]:
        op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # User.username
    if 'ix_users_username' not in [idx['name'] for idx in inspector.get_indexes('users')]:
        op.create_index('ix_users_username', 'users',
                        ['username'], unique=True)

    # Article.slug
    if 'ix_articles_slug' not in [idx['name'] for idx in inspector.get_indexes('articles')]:
        op.create_index('ix_articles_slug', 'articles', ['slug'], unique=True)

    # Tag.name
    if 'ix_tags_name' not in [idx['name'] for idx in inspector.get_indexes('tags')]:
        op.create_index('ix_tags_name', 'tags', ['name'], unique=True)


def downgrade() -> None:
    """Удаляем уникальные индексы, если они существуют."""
    conn = op.get_bind()
    inspector = inspect(conn)

    # User.email
    if 'ix_users_email' in [idx['name'] for idx in inspector.get_indexes('users')]:
        op.drop_index('ix_users_email', table_name='users')

    # User.username
    if 'ix_users_username' in [idx['name'] for idx in inspector.get_indexes('users')]:
        op.drop_index('ix_users_username', table_name='users')

    # Article.slug
    if 'ix_articles_slug' in [idx['name'] for idx in inspector.get_indexes('articles')]:
        op.drop_index('ix_articles_slug', table_name='articles')

    # Tag.name
    if 'ix_tags_name' in [idx['name'] for idx in inspector.get_indexes('tags')]:
        op.drop_index('ix_tags_name', table_name='tags')
