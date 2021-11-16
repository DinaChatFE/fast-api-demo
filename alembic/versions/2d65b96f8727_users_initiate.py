"""users initiate

Revision ID: 2d65b96f8727
Revises: 346f5bc77637
Create Date: 2021-11-09 12:40:24.123276

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean


# revision identifiers, used by Alembic.
revision = '2d65b96f8727'
down_revision = '346f5bc77637'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users' ,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('users')
