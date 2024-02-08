"""“added_referral”

Revision ID: 2679aa8ffee5
Revises: 1580f0606fb8
Create Date: 2024-02-08 11:43:56.882144

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2679aa8ffee5'
down_revision: Union[str, None] = '1580f0606fb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('referral', sa.String(), nullable=True))
    op.create_unique_constraint(op.f('users_email_key'), 'users', ['email'])
    op.create_unique_constraint(op.f('users_referral_key'), 'users', ['referral'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('users_referral_key'), 'users', type_='unique')
    op.drop_constraint(op.f('users_email_key'), 'users', type_='unique')
    op.drop_column('users', 'referral')
    # ### end Alembic commands ###