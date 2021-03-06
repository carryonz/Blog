"""empty message

Revision ID: b6f22347fad0
Revises: 8ce38dc77671
Create Date: 2019-01-16 20:35:37.406398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b6f22347fad0'
down_revision = '8ce38dc77671'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('uid', sa.Integer(), nullable=True))
    op.drop_index('logo', table_name='blog')
    op.drop_constraint('blog_ibfk_1', 'blog', type_='foreignkey')
    op.create_foreign_key(None, 'blog', 'user', ['uid'], ['id'])
    op.drop_column('blog', 'logo')
    op.drop_column('blog', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('author', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('blog', sa.Column('logo', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'blog', type_='foreignkey')
    op.create_foreign_key('blog_ibfk_1', 'blog', 'user', ['author'], ['username'])
    op.create_index('logo', 'blog', ['logo'], unique=True)
    op.drop_column('blog', 'uid')
    # ### end Alembic commands ###
