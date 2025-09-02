"""
Dependency injection module for chat-related services
"""

from fastapi import Depends
from langchain_core.runnables import RunnableSerializable
from langgraph.graph.state import CompiledStateGraph

from ai_agent.api.dependencies.chain_dependencies import \
    get_generate_session_name_chain
from ai_agent.api.dependencies.graph_dependencies import get_graph
from ai_agent.api.dependencies.repository_dependencies import (
    get_chat_session_repository, get_collection_repository,
    get_history_message_repository, get_organization_repository)
from ai_agent.application.services.chat_service import ChatService
from ai_agent.infrastructure.database.repositories import (
    BaseChatSessionRepository, BaseCollectionRepository,
    BaseHistoryMessageRepository, BaseOrganizationRepository)


def get_chat_service(
    graph: CompiledStateGraph = Depends(get_graph),
    history_message_repository: BaseHistoryMessageRepository = Depends(
        get_history_message_repository
    ),
    organization_repository: BaseOrganizationRepository = Depends(
        get_organization_repository
    ),
    chat_session_repository: BaseChatSessionRepository = Depends(
        get_chat_session_repository
    ),
    collection_repository: BaseCollectionRepository = Depends(
        get_collection_repository
    ),
    generate_session_name_chain: RunnableSerializable = Depends(
        get_generate_session_name_chain
    ),
) -> ChatService:
    """
    Factory function that provides a configured ChatService instance.

    Args:
        graph (CompiledStateGraph): The agent graph, injected via dependency
        history_message_repository (BaseHistoryMessageRepository):
            The history message service, injected via dependency
        organization_repository (BaseOrganizationRepository):
            repository for organization table
        chat_session_repository (BaseChatSessionRepository):
            service to work with chat session
        collection_repository (BaseCollectionRepository):
            repository for collection table
        generate_session_name_chain (RunnableSerializable): LLM chain

    Returns:
        ChatService: A configured chat service ready to process messages
    """
    return ChatService(
        graph,
        history_message_repository,
        organization_repository,
        chat_session_repository,
        collection_repository,
        generate_session_name_chain
    )
