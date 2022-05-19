"""auto add votes table

Revision ID: a8ca010bf3ff
Revises: fdd741fcf825
Create Date: 2022-05-19 14:45:52.373183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8ca010bf3ff'
down_revision = 'fdd741fcf825'
branch_labels = None
depends_on = None


def upgrade():
    print("SKip")
    pass


def downgrade():
    print("Skip")
    pass
