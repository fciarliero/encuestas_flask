"""empty message

Revision ID: 0cdbec7641f6
Revises: 
Create Date: 2020-11-22 20:02:25.298168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cdbec7641f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('poll',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_poll_expiration'), 'poll', ['expiration'], unique=False)
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('option1', sa.String(length=128), nullable=True),
    sa.Column('option2', sa.String(length=128), nullable=True),
    sa.Column('option3', sa.String(length=128), nullable=True),
    sa.Column('option4', sa.String(length=128), nullable=True),
    sa.Column('correct_answer', sa.String(length=128), nullable=True),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent'], ['poll.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('question', sa.Integer(), nullable=True),
    sa.Column('result', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['question'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_index(op.f('ix_poll_expiration'), table_name='poll')
    op.drop_table('poll')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
