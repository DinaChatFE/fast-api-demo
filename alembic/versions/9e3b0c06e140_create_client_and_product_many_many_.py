"""create client and product many many relationships

Revision ID: 9e3b0c06e140
Revises: b0926d8a629e
Create Date: 2021-11-10 20:14:51.200559

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = '9e3b0c06e140'
down_revision = 'b0926d8a629e'
branch_labels = None
depends_on = None


def upgrade():
    """create clients tables"""
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer ,primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('phone_number', sa.String , nullable=True),
        sa.Column('is_verification', sa.Boolean ,default=True),
        sa.Column('created_at', sa.TIMESTAMP, default=datetime.utcnow)
    )
    """Create products tables"""
    op.create_table(
        'products',
        sa.Column("id", sa.Integer ,primary_key=True),
        sa.Column('title', sa.String,  nullable=False),
        sa.Column('price', sa.Float, default=0.0),
        sa.Column('created_at', sa.TIMESTAMP, default=datetime.utcnow)
        
    )
    """Create third party table to connect constrain of two tables"""
    op.create_table(
        'client_product',
        sa.Column('client_id', sa.Integer),
        sa.Column('product_id', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP, default=datetime.utcnow)
    )

def downgrade():
    op.drop_table("clients")
    op.drop_table("products")
    op.drop_table("client_product")
