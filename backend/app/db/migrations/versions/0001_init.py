from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Extension for gen_random_uuid if needed in future
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    # Users
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=32), nullable=False, server_default='user'),
        sa.Column('timezone', sa.String(length=64), nullable=False, server_default='Asia/Nicosia'),
        sa.Column('email_verified', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('password_hash', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Auth identities
    op.create_table('auth_identities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provider', sa.String(length=64), nullable=False),
        sa.Column('provider_user_id', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_auth_provider_user', 'auth_identities', ['provider_user_id'], unique=False)

    # Interests
    op.create_table('interests',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tag', sa.String(length=128), nullable=False),
        sa.Column('weight', sa.Float, nullable=False, server_default='1'),
        sa.Column('source_hint', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_interests_user_tag', 'interests', ['user_id','tag'], unique=False)

    # Sources
    op.create_table('sources',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(length=64), nullable=False, unique=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='inactive'),
        sa.Column('last_success_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_sources_key', 'sources', ['key'], unique=True)

    # Trend items
    op.create_table('trend_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('source_id', sa.Integer, sa.ForeignKey('sources.id', ondelete='SET NULL'), nullable=True),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=512), nullable=False),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('platform', sa.String(length=64), nullable=False),
        sa.Column('creator_handle', sa.String(length=128), nullable=True),
        sa.Column('metrics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('dedupe_hash', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dedupe_hash', name='uq_trend_items_dedupe_hash')
    )
    op.create_index('ix_trend_items_external_id', 'trend_items', ['external_id'], unique=False)

    # Rankings
    op.create_table('rankings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trend_item_id', sa.Integer, sa.ForeignKey('trend_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('global_rank', sa.Integer, nullable=True),
        sa.Column('per_topic_rank', sa.Integer, nullable=True),
        sa.Column('score', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # User trend scores
    op.create_table('user_trend_scores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('trend_item_id', sa.Integer, sa.ForeignKey('trend_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('score', sa.Float, nullable=True),
        sa.Column('reason', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Prompts
    op.create_table('prompts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('trend_item_id', sa.Integer, sa.ForeignKey('trend_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(length=16), nullable=False),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('model_hint', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Deliveries
    op.create_table('deliveries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('mode', sa.String(length=16), nullable=False),
        sa.Column('subject', sa.Text, nullable=True),
        sa.Column('body_html', sa.Text, nullable=True),
        sa.Column('body_text', sa.Text, nullable=True),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Schedules
    op.create_table('schedules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cadence', sa.String(length=16), nullable=False),
        sa.Column('hour', sa.Integer, nullable=False, server_default='9'),
        sa.Column('minute', sa.Integer, nullable=False, server_default='0'),
        sa.Column('enabled', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Audit log
    op.create_table('audit_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('entity', sa.String(length=64), nullable=False),
        sa.Column('entity_id', sa.String(length=64), nullable=True),
        sa.Column('action', sa.String(length=64), nullable=False),
        sa.Column('by_user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Trigger to auto-update updated_at on UPDATE for tables that have it
    for table in ['users','interests','sources','schedules']:
        op.execute(f"""
        CREATE OR REPLACE FUNCTION update_{table}_updated_at() RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_{table}_updated_at
        BEFORE UPDATE ON {table}
        FOR EACH ROW EXECUTE FUNCTION update_{table}_updated_at();
        """)

def downgrade():
    for table in ['users','interests','sources','schedules']:
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};")
        op.execute(f"DROP FUNCTION IF EXISTS update_{table}_updated_at();")
    op.drop_table('audit_log')
    op.drop_table('schedules')
    op.drop_table('deliveries')
    op.drop_table('prompts')
    op.drop_table('user_trend_scores')
    op.drop_table('rankings')
    op.drop_table('trend_items')
    op.drop_table('sources')
    op.drop_index('ix_interests_user_tag', table_name='interests')
    op.drop_table('interests')
    op.drop_index('ix_auth_provider_user', table_name='auth_identities')
    op.drop_table('auth_identities')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
