"""empty message

Revision ID: 2159f4087651
Revises: 372a3ca7c929
Create Date: 2019-05-30 12:09:36.554037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2159f4087651'
down_revision = '372a3ca7c929'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('updated_at', sa.TIMESTAMP(), nullable=True))
    op.create_index(op.f('ix_images_updated_at'), 'images', ['updated_at'], unique=False)
    op.drop_column('posts', 'version')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('version', sa.BIGINT(), nullable=True))
    op.drop_index(op.f('ix_images_updated_at'), table_name='images')
    op.drop_column('images', 'updated_at')
    # ### end Alembic commands ###
