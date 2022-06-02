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
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('Users')
