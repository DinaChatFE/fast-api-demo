"""customer

Revision ID: b0926d8a629e
Revises: 2d65b96f8727
Create Date: 2021-11-09 13:06:28.875233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.type_api import INTEGERTYPE


# revision identifiers, used by Alembic.
revision = 'b0926d8a629e'
down_revision = '2d65b96f8727'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer ,primary_key=True),
        sa.Column('is_famous', sa.Boolean, nullable=True),
        sa.Column('shop_name', sa.String, nullable=True),
        sa.Column('user_id', sa.Integer, nullable=False )
    )


def downgrade():
    op.drop_table('customers')
