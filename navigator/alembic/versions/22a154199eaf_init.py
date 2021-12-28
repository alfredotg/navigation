"""init

Revision ID: 22a154199eaf
Revises: 
Create Date: 2021-12-31 06:52:06.821006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22a154199eaf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('point',
    sa.Column('point_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('point_id', name=op.f('pk__point'))
    )
    op.create_table('route',
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('from_id', sa.Integer(), nullable=False),
    sa.Column('to_id', sa.Integer(), nullable=False),
    sa.Column('distance', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('route_id', name=op.f('pk__route'))
    )
    op.create_table('route_step',
    sa.Column('step_id', sa.Integer(), nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.Column('point_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['route_id'], ['route.route_id'], name=op.f('fk__route_step__route_id__route')),
    sa.PrimaryKeyConstraint('step_id', name=op.f('pk__route_step'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('route_step')
    op.drop_table('route')
    op.drop_table('point')
    # ### end Alembic commands ###
