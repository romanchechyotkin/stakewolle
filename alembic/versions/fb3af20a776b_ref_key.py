"""“ref_key”

Revision ID: fb3af20a776b
Revises: d157b6689a0c
Create Date: 2024-02-09 16:32:33.309014

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fb3af20a776b'
down_revision: Union[str, None] = 'd157b6689a0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_referral_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_referral_key', 'users', ['referral'])
    # ### end Alembic commands ###