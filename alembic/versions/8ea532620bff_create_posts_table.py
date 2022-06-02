"""create Posts table

Revision ID: 8ea532620bff
Revises: 
Create Date: 2022-05-19 13:22:25.675714

"""
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ea532620bff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('Posts')
    pass
