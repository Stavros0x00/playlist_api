"""bigger artist  name field for tracks

Revision ID: a4860ec7676a
Revises: 15bc45194838
Create Date: 2017-12-31 15:06:08.389623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4860ec7676a'
down_revision = '15bc45194838'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tracks', 'artist',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=600),
               existing_nullable=True)
    op.alter_column('tracks', 'name',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=300),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tracks', 'name',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    op.alter_column('tracks', 'artist',
               existing_type=sa.String(length=600),
               type_=sa.VARCHAR(length=300),
               existing_nullable=True)
    # ### end Alembic commands ###