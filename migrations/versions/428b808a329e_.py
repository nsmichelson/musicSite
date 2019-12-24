"""empty message

Revision ID: 428b808a329e
Revises: 3eb01954957e
Create Date: 2019-12-23 15:26:00.200726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '428b808a329e'
down_revision = '3eb01954957e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('start_time', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'start_time')
    # ### end Alembic commands ###
