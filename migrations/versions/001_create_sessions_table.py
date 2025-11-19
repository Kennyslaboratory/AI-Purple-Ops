"""Create sessions table

Revision ID: 001
Revises: 
Create Date: 2025-11-19

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create captured_requests table for traffic capture."""
    op.execute("""
        CREATE TABLE IF NOT EXISTS captured_requests (
            id BIGINT PRIMARY KEY,
            session_id TEXT NOT NULL,
            ts TIMESTAMP NOT NULL,
            method TEXT NOT NULL,
            url TEXT NOT NULL,
            request_headers JSON,
            request_body BLOB,
            request_is_base64 BOOLEAN DEFAULT FALSE,
            status INTEGER,
            response_headers JSON,
            response_body BLOB,
            response_is_base64 BOOLEAN DEFAULT FALSE,
            response_time_ms INTEGER,
            server_ip TEXT,
            model_response_json JSON,
            evidence_tags JSON
        )
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_captured_requests_session_ts 
        ON captured_requests(session_id, ts)
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_captured_requests_session 
        ON captured_requests(session_id)
    """)
    
    # Create session index table for quick listing
    op.execute("""
        CREATE TABLE IF NOT EXISTS session_index (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP NOT NULL,
            adapter_name TEXT,
            model TEXT,
            test_suite TEXT,
            request_count INTEGER DEFAULT 0,
            metadata JSON
        )
    """)


def downgrade() -> None:
    """Drop tables."""
    op.execute("DROP INDEX IF EXISTS idx_captured_requests_session")
    op.execute("DROP INDEX IF EXISTS idx_captured_requests_session_ts")
    op.execute("DROP TABLE IF EXISTS captured_requests")
    op.execute("DROP TABLE IF EXISTS session_index")

