"""init

Revision ID: 346f5bc77637
Revises: 
Create Date: 2021-11-05 22:20:09.486262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '346f5bc77637'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'jobs', 
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True)
    )

def downgrade():
    op.drop_column('jobs')
