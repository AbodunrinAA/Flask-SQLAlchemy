"""empty message

Revision ID: b81b47c7b416
Revises: 
Create Date: 2022-08-31 16:29:50.170168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b81b47c7b416'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Businesses',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Stores',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('number', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('business_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['Businesses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Items',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('produce_date', sa.DateTime(), nullable=True),
    sa.Column('expire_date', sa.DateTime(), nullable=True),
    sa.Column('price', sa.Float(precision=5), nullable=True),
    sa.Column('store_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['Stores.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=True),
    sa.Column('lastname', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('store_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['Stores.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    op.drop_table('Items')
    op.drop_table('Stores')
    op.drop_table('Businesses')
    # ### end Alembic commands ###
