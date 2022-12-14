"""first

Revision ID: 6a60165c54a2
Revises: 
Create Date: 2022-09-22 03:08:35.927445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a60165c54a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Account',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('currency_name', sa.String(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('user_deposit', sa.Integer(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency_name', sa.String(), nullable=False),
    sa.Column('cost_concerning_USD', sa.Integer(), nullable=False),
    sa.Column('available_quantity', sa.Integer(), nullable=False),
    sa.Column('datatime', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Deposit',
    sa.Column('deposit_ID', sa.Integer(), nullable=False),
    sa.Column('opening_date', sa.String(), nullable=False),
    sa.Column('closing_date', sa.String(), nullable=False),
    sa.Column('value_name', sa.String(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('interest_rate', sa.Integer(), nullable=False),
    sa.Column('info', sa.String(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('deposit_ID')
    )
    op.create_table('History',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('history', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Rating',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cur_name', sa.String(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Transfer',
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('type_of_transaction', sa.String(), nullable=False),
    sa.Column('amount_of_currency_spent', sa.Float(), nullable=False),
    sa.Column('from_what_currency', sa.String(), nullable=False),
    sa.Column('in_what_currency', sa.String(), nullable=False),
    sa.Column('data_and_time', sa.String(), nullable=False),
    sa.Column('the_ammount_of_currency', sa.Float(), nullable=False),
    sa.Column('comission', sa.Integer(), nullable=True),
    sa.Column('donor_account', sa.Integer(), nullable=False),
    sa.Column('beneficiary_account', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trade_id', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    op.drop_table('Transfer')
    op.drop_table('Rating')
    op.drop_table('History')
    op.drop_table('Deposit')
    op.drop_table('Currency')
    op.drop_table('Account')
    # ### end Alembic commands ###
