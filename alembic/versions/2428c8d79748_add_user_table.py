"""add User table

Revision ID: 2428c8d79748
Revises: dba756463b2f
Create Date: 2022-05-19 14:11:49.325419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2428c8d79748'
down_revision = 'dba756463b2f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Users', sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('Email', sa.String(400), nullable=False), sa.Column('Password', sa.String(), nullable=False), sa.Column('Created_At', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False), sa.PrimaryKeyConstraint('Id'), sa.UniqueConstraint('Email'))


def downgrade():
    op.drop_table('Users')
