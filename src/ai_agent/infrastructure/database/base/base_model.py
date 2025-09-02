"""
Base model definition for SQLAlchemy ORM models.

This module defines the shared declarative base that all ORM models should inherit from.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
