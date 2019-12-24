"""empty message

Revision ID: b6ee5fc2841a
Revises: 428b808a329e
Create Date: 2019-12-23 15:41:11.253707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6ee5fc2841a'
down_revision = '428b808a329e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###