"""
This module provides a concrete implementation of BaseAppClientRepository,
using SQLAlchemy ORM for performing CRUD operations on AppClient entities.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ai_agent.domain.dtos.app_client_dto import (AppClientCreateDTO,
                                                 AppClientUpdateDTO)
from ai_agent.domain.models.database_entities.app_client import AppClient
from ai_agent.infrastructure.database.models.app_client_model import \
    AppClientModel
from ai_agent.infrastructure.database.models.collection_model import \
    CollectionModel

from .base_app_client_repository import BaseAppClientRepository


class AppClientRepository(BaseAppClientRepository):
    """
    Repository class for AppClient model
    """

    def __init__(self, session: Session):
        """
        Initialize the AppClientRepository with a database session.

        Args:
            session (Session): SQLAlchemy database session.
        """
        self.session = session

    def get_by_client_id(
        self,
        client_id: UUID,
    ) -> Optional[AppClient]:
        """
        Retrieve a single AppClient by client_id, scoped to a specific organization.

        Parameters:
            client_id (UUID): The unique identifier of the AppClient to retrieve.

        Returns:
            Optional[AppClient]: The AppClient object if found, otherwise None.
        """
        statement = (
            select(AppClientModel)
            .where(
                AppClientModel.client_id == client_id,
            )
        )
        result = self.session.execute(statement).scalar_one_or_none()
        return AppClient.from_db_model(result) if result else None

    def get_by_name(
            self,
            name: str,
            organization_id: UUID
        ) -> Optional[AppClient]:
        """
        Retrieve an AppClient by its name within a specific organization.

        Parameters:
            name (str): The name of the AppClient to retrieve.
            organization_id (UUID): The unique identifier of the organization
                to which the AppClient belongs.

        Returns:
            Optional[AppClient]: The AppClient object if found within the specified organization,
                otherwise None.
        """
        statement = select(AppClientModel).where(
            and_(
                AppClientModel.name == name,
                AppClientModel.organization_id == organization_id
            )
        )
        result = self.session.execute(statement).scalar_one_or_none()
        return AppClient.from_db_model(result) if result else None

    def exists(self, name: str, organization_id: UUID) -> bool:
        """
        Check if an AppClient with the given name already exists in the organization.

        Parameters:
            name (str): The name of the AppClient to check.
            organization_id (UUID): The organization in which to check.

        Returns:
            bool: True if an AppClient with the given name exists, False otherwise.
        """
        statement = select(AppClientModel.client_id).where(
            and_(
                AppClientModel.name == name,
                AppClientModel.organization_id == organization_id
            )
        ).limit(1)
        result = self.session.execute(statement).scalar_one_or_none()
        return result is not None



    def list_by_organization(self, organization_id: UUID) -> List[AppClient]:
        """
        Retrieve all AppClients for a given organization.

        Args:
            organization_id (UUID): The organization to filter by.

        Returns:
            List[AppClient]: All AppClients for the organization.
        """
        statement = select(AppClientModel).where(
            AppClientModel.organization_id == organization_id
        )
        results = self.session.execute(statement).scalars().all()
        return [AppClient.from_db_model(r) for r in results]

    def create(
        self,
        data: AppClientCreateDTO,
        organization_id: UUID
    ) -> AppClient:
        """
        Create a new AppClient under the specified organization.

        Args:
            data (AppClientCreateDTO): The data to create the AppClient.
            organization_id (UUID): The organization the AppClient belongs to.

        Returns:
            AppClient: The newly created AppClient.
        """
        # Get collection_ids
        collection_ids = data.collection_ids
        client_data = data.model_dump(exclude={"collection_ids"})

        # Query collections
        collections = self.session.query(CollectionModel).filter(
            CollectionModel.id.in_(collection_ids),
            CollectionModel.organization_id == organization_id
        ).all()

        # Create AppClientModel
        db_object = AppClientModel(
            **client_data,
            organization_id=organization_id,
            collections=collections
        )
        self.session.add(db_object)
        self.session.commit()
        self.session.refresh(db_object)
        return AppClient.from_db_model(db_object)

    def update(
        self,
        client_id: UUID,
        organization_id: UUID,
        data: AppClientUpdateDTO
    ) -> Optional[AppClient]:
        """
        Update an AppClient within the specified organization.

        Args:
            client_id (UUID): ID of the AppClient to update.
            organization_id (UUID): Organization the AppClient belongs to.
            data (AppClientUpdateDTO): Fields to update.

        Returns:
            Optional[AppClient]: Updated AppClient if found, otherwise None.
        """
        # Fetch the existing AppClient by ID and organization
        statement = (
            select(AppClientModel)
            .where(
                and_(
                    AppClientModel.client_id == client_id,
                    AppClientModel.organization_id == organization_id,
                )
            )
        )
        db_object = self.session.execute(statement).scalar_one_or_none()
        if not db_object:
            return None

        # extract collection_ids
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        collection_ids = update_data.pop("collection_ids", None)

        # Apply standard field updates
        for key, value in update_data.items():
            setattr(db_object, key, value)

        # If collection_ids were provided, update the M:N relationship
        if collection_ids is not None:
            collections = self.session.query(CollectionModel).filter(
                CollectionModel.id.in_(collection_ids),
                CollectionModel.organization_id == organization_id
            ).all()
            db_object.collections = collections

        # Commit changes and return updated model
        self.session.commit()
        self.session.refresh(db_object)
        return AppClient.from_db_model(db_object)


    def delete(self, client_id: UUID, organization_id: UUID) -> None:
        """
        Delete an AppClient if it belongs to the specified organization.

        Args:
            client_id (UUID): ID of the AppClient to delete.
            organization_id (UUID): Organization the AppClient belongs to.

        Returns:
            None
        """
        statement = (
            select(AppClientModel)
            .where(
                and_(
                    AppClientModel.client_id == client_id,
                    AppClientModel.organization_id == organization_id,
                )
            )
        )
        db_object = self.session.execute(statement).scalar_one_or_none()
        if not db_object:
            return
        self.session.delete(db_object)
        self.session.commit()
