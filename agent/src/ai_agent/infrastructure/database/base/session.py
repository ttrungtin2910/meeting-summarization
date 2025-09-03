"""
Session management for SQLAlchemy using SQLStorageConfig.

This module automates the creation of engine and session management
for easier and safer database interactions.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ai_agent.config import VectorStoreConfig
from ai_agent.utilities.url_utils import create_connection_url

CONNECTION_URL = create_connection_url(VectorStoreConfig)

engine = create_engine(CONNECTION_URL, echo=False)

session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """
    Creates and yields a database session, ensuring proper cleanup.

    Yields:
        Session: Database session object

    Notes:
        - Automatically rolls back transactions on exceptions
        - Always closes the session when done
    """
    db = session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
