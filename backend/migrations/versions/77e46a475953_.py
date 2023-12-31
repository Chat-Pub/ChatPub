"""empty message

Revision ID: 77e46a475953
Revises: 8ba3b1821556
Create Date: 2023-11-16 15:18:05.014348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '77e46a475953'
down_revision: Union[str, None] = '8ba3b1821556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('userinfo', 'birth',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=16),
               existing_nullable=False)
    op.alter_column('userinfo', 'money',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('userinfo', 'money',
               existing_type=sa.String(length=255),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    op.alter_column('userinfo', 'birth',
               existing_type=sa.String(length=16),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    # ### end Alembic commands ###
