"""add foreign key to posts table

Revision ID: fdd741fcf825
Revises: 2428c8d79748
Create Date: 2022-05-19 14:25:20.904883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdd741fcf825'
down_revision = '2428c8d79748'
branch_labels = None
depends_on = None

# ADDING A FOREIGN KEY TO A TABLE, source_table is the table where the foreign key will be created


def upgrade():
    op.add_column("Posts", sa.Column('User_Id', sa.Integer(), nullable=False))
    op.create_foreign_key('Posts_Users_fk', source_table="Posts", referent_table="Users", local_cols=[
                          "User_Id"], remote_cols=["Id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('Posts_Users_fk', table_name="Posts")
    op.drop_column("Posts", "User_Id")
    pass
