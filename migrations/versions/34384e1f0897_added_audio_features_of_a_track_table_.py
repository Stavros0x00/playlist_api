"""added audio features of a track table and relathionships

Revision ID: 34384e1f0897
Revises: 0045fe0c4ced
Create Date: 2018-04-28 16:24:10.643068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34384e1f0897'
down_revision = '0045fe0c4ced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track_features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=True),
    sa.Column('acousticness', sa.Float(), nullable=True),
    sa.Column('danceability', sa.Float(), nullable=True),
    sa.Column('duration_ms', sa.Integer(), nullable=True),
    sa.Column('energy', sa.Float(), nullable=True),
    sa.Column('instrumentalness', sa.Float(), nullable=True),
    sa.Column('key', sa.Integer(), nullable=True),
    sa.Column('liveness', sa.Float(), nullable=True),
    sa.Column('loudness', sa.Float(), nullable=True),
    sa.Column('mode', sa.Integer(), nullable=True),
    sa.Column('speechiness', sa.Float(), nullable=True),
    sa.Column('tempo', sa.Float(), nullable=True),
    sa.Column('time_signature', sa.Integer(), nullable=True),
    sa.Column('valence', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_features')
    # ### end Alembic commands ###
