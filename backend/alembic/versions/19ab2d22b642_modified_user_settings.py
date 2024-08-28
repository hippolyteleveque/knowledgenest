"""Modified user settings.

Revision ID: 19ab2d22b642
Revises: 5928b145547a
Create Date: 2024-08-28 09:40:57.050409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19ab2d22b642'
down_revision: Union[str, None] = '5928b145547a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_setting_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'setting_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('setting_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_setting_id_fkey', 'users', 'user_settings', ['setting_id'], ['id'])
    # ### end Alembic commands ###
