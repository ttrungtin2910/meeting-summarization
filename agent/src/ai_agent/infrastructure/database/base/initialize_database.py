"""
Database initialization script.

This module initializes the database schema by creating all tables
defined in the application models. It should be run once before
starting the application for the first time or after schema changes.
"""

from dotenv import load_dotenv

# pylint: disable=wrong-import-position
# Load environment variables
load_dotenv()

from sqlalchemy import text

from ai_agent.infrastructure.database.base.base_model import Base
from ai_agent.infrastructure.database.base.session import engine
from ai_agent.infrastructure.database.models import *  # pylint: disable=wildcard-import, unused-wildcard-import


def init_db(db_engine):
    """
    Initialize the database by creating all defined tables.

    This function creates all tables that are defined in the application's
    SQLAlchemy models and registered with the Base metadata.

    Args:
        db_engine: SQLAlchemy engine instance connected to the target database.

    Returns:
        None
    """
    print("Creating all tables...")
    Base.metadata.create_all(bind=db_engine)
    print("Done creating tables")

    with db_engine.connect() as conn:
        print("Creating ivfflat index for embeddings.embedding...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_embeddings_vector_cosine
            ON embeddings USING ivfflat (embedding vector_cosine_ops);
        """))
        conn.commit()
        print("Index created.")


if __name__ == "__main__":
    # Initialize the database
    init_db(engine)
