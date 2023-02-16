"""empty message

Revision ID: fbb69bbd9312
Revises: 
Create Date: 2023-02-16 22:26:30.181941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbb69bbd9312'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('size', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('original_filename', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('original_filename')
    )
    op.create_table('word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transcript',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('IN_PROGRESS', 'SUCCESS', 'FAILURE', name='transcriptstatusenum'), nullable=False),
    sa.Column('audio_id', sa.Integer(), nullable=True),
    sa.Column('external_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['audio_id'], ['audio.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id', name='one_external_id')
    )
    op.create_table('transcriptitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transcript_id', sa.Integer(), nullable=True),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.Column('start_at', sa.Integer(), nullable=True),
    sa.Column('stop_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['transcript_id'], ['transcript.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transcriptitem')
    op.drop_table('transcript')
    op.drop_table('word')
    op.drop_table('audio')
    # ### end Alembic commands ###
