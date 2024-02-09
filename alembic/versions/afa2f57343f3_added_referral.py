"""“added_referral”

Revision ID: afa2f57343f3
Revises: 2679aa8ffee5
Create Date: 2024-02-09 16:09:40.298949

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'afa2f57343f3'
down_revision: Union[str, None] = '2679aa8ffee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('referral_codes',
    sa.Column('code', sa.String(length=12), nullable=False),
    sa.Column('expiration', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('code', name=op.f('referral_codes_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referral_codes')
    # ### end Alembic commands ###