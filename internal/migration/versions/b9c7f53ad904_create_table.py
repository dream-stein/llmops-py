"""create_table

Revision ID: b9c7f53ad904
Revises: 
Create Date: 2026-02-01 20:57:12.366472

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b9c7f53ad904'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        'app',
        sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('account_id', sa.UUID(), nullable=True),
        sa.Column(
            'name',
            sa.String(length=255),
            nullable=False,
            server_default=sa.text("''::character varying"),
        ),
        sa.Column(
            'icon',
            sa.String(length=255),
            nullable=False,
            server_default=sa.text("''::character varying"),
        ),
        sa.Column(
            'description',
            sa.Text(),
            nullable=False,
            server_default=sa.text("''::text"),
        ),
        sa.Column(
            'status',
            sa.String(length=255),
            nullable=False,
            server_default=sa.text("''::character varying"),
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP(0)'),
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP(0)'),
        ),
        sa.PrimaryKeyConstraint('id', name='pk_app_id'),
    )
    with op.batch_alter_table('app', schema=None) as batch_op:
        batch_op.create_index('idx_app_account_id', ['account_id'], unique=False)


def downgrade():
    with op.batch_alter_table('app', schema=None) as batch_op:
        batch_op.drop_index('idx_app_account_id')

    op.drop_table('app')
