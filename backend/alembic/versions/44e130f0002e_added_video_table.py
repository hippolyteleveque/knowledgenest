"""Added video table.

Revision ID: 44e130f0002e
Revises: 9a062181b1df
Create Date: 2024-08-21 22:35:16.783925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44e130f0002e'
down_revision: Union[str, None] = '9a062181b1df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('videos',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('imageUrl', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('publishDate', sa.Date(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_videos_url'), 'videos', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_videos_url'), table_name='videos')
    op.drop_table('videos')
    # ### end Alembic commands ###
