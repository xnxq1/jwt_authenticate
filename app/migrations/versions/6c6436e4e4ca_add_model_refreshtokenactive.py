"""Add model RefreshTokenActive

Revision ID: 6c6436e4e4ca
Revises: 2c55b8e2bb57
Create Date: 2024-08-30 00:04:39.631946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c6436e4e4ca'
down_revision: Union[str, None] = '2c55b8e2bb57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RefreshTokenActive',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('RefreshTokenActive')
    # ### end Alembic commands ###
