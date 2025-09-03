"""
This module provides a concrete implementation of BaseAdminRepository,
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_agent.domain.models.database_entities.admin import Admin
from ai_agent.infrastructure.database.models.admin_model import AdminModel

from .base_admin_repository import BaseAdminRepository


class AdminRepository(BaseAdminRepository):
    """
    Repository class for Admin model
    """

    def __init__(self, session: Session):
        """
        Initialize the AdminRepository with a database session.

        Args:
            session (Session): SQLAlchemy database session.
        """
        self.session = session

    def get_by_email(self, email: str) -> Optional[Admin]:
        """
        Retrieves an Admin entity by their email address.

        Args:
            email (str): The email address of the Admin to retrieve.

        Returns:
            Optional[Admin]: The Admin entity if found, otherwise None.
        """
        statement = (
            select(AdminModel)
            .where(AdminModel.email == email)
        )
        result: Optional[AdminModel] = self.session.execute(statement).scalar_one_or_none()
        return Admin.model_validate(result) if result else None
