"""Adding municipals

Revision ID: ccd69623c86a
Revises: 3e0a23c3bea8
Create Date: 2022-07-08 18:34:43.994407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccd69623c86a'
down_revision = '3e0a23c3bea8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('municipal',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('district_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_municipal_district_id'), 'municipal', ['district_id'], unique=False)
    op.create_index(op.f('ix_municipal_id'), 'municipal', ['id'], unique=False)
    op.create_index(op.f('ix_municipal_name'), 'municipal', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_municipal_name'), table_name='municipal')
    op.drop_index(op.f('ix_municipal_id'), table_name='municipal')
    op.drop_index(op.f('ix_municipal_district_id'), table_name='municipal')
    op.drop_table('municipal')
    # ### end Alembic commands ###