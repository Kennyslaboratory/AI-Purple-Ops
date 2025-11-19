"""Create payloads tables

Revision ID: 002
Revises: 001
Create Date: 2025-11-19

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create payload tables with provenance and tags."""
    
    # Payload sources table
    op.execute("""
        CREATE TABLE IF NOT EXISTS payload_sources (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            version TEXT,
            license TEXT,
            url TEXT,
            sha256 TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Main payloads table
    op.execute("""
        CREATE TABLE IF NOT EXISTS payloads (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            category TEXT,
            sub_category TEXT,
            source_id TEXT,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP,
            last_success_at TIMESTAMP,
            success_count INTEGER DEFAULT 0,
            total_count INTEGER DEFAULT 0,
            metadata JSON,
            FOREIGN KEY (source_id) REFERENCES payload_sources(id)
        )
    """)
    
    # Many-to-many tags table
    op.execute("""
        CREATE TABLE IF NOT EXISTS payload_tags (
            payload_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            PRIMARY KEY (payload_id, tag),
            FOREIGN KEY (payload_id) REFERENCES payloads(id) ON DELETE CASCADE
        )
    """)
    
    # Indexes for performance
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_payloads_category 
        ON payloads(category)
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_payloads_source 
        ON payloads(source_id)
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_payload_tags_tag 
        ON payload_tags(tag)
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_payload_tags_payload 
        ON payload_tags(payload_id)
    """)


def downgrade() -> None:
    """Drop payload tables."""
    op.execute("DROP INDEX IF EXISTS idx_payload_tags_payload")
    op.execute("DROP INDEX IF EXISTS idx_payload_tags_tag")
    op.execute("DROP INDEX IF EXISTS idx_payloads_source")
    op.execute("DROP INDEX IF EXISTS idx_payloads_category")
    op.execute("DROP TABLE IF EXISTS payload_tags")
    op.execute("DROP TABLE IF EXISTS payloads")
    op.execute("DROP TABLE IF EXISTS payload_sources")

