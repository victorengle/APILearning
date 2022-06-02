"""add columns to Posts table

Revision ID: dba756463b2f
Revises: 8ea532620bff
Create Date: 2022-05-19 13:44:08.098460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dba756463b2f'
down_revision = '8ea532620bff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('Posts', 'Created_At')
    pass
