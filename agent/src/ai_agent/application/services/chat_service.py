"""
Chat Service Module.

It handles the conversion and processes interactions by invoking the agent graph.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableSerializable
from langgraph.graph.state import CompiledStateGraph

from ai_agent.application.graph.state import AgentState
from ai_agent.domain.dtos.chat_session_dto import ChatSessionUpdateDTO
from ai_agent.domain.dtos.history_message_dto import HistoryMessageCreateDTO
from ai_agent.domain.exceptions.chat_session_exceptions import \
    ChatSessionNotFound
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.exceptions.message_exceptions import MessageNotFound
from ai_agent.domain.models.database_entities.chat_session import ChatSession
from ai_agent.domain.models.database_entities.history_message import \
    HistoryMessage
from ai_agent.domain.models.security_contexts.client_context import \
    ClientContext
from ai_agent.domain.value_objects.chat_message import ChatMessage
from ai_agent.infrastructure.database.repositories import (
    BaseChatSessionRepository, BaseCollectionRepository,
    BaseHistoryMessageRepository, BaseOrganizationRepository)
from ai_agent.infrastructure.mappers.langchain_message_mapper import (
    convert_from_langchain_message, convert_to_langchain_messages)


class ChatService:
    """
    Service for processing chat interactions through the agent graph.

    This service manages the interaction between the API layer and the agent graph,
    handling message conversion, state management, and graph execution.
    """

    def __init__(
            self,
            graph: CompiledStateGraph,
            history_message_repository: BaseHistoryMessageRepository,
            organization_repository: BaseOrganizationRepository,
            chat_session_repository: BaseChatSessionRepository,
            collection_repository: BaseCollectionRepository,
            generate_session_name_chain: RunnableSerializable
        ) -> None:
        """
        Initialize the ChatService with a compiled agent graph.

        Args:
            graph (CompiledStateGraph): The LangGraph agent graph to handle message processing
            history_message_repository (BaseHistoryMessageRepository):
                repository to work with history messages
            organization_repository (BaseOrganizationRepository): repository for organization table
            chat_session_repository (BaseChatSessionRepository):
                repository to work with chat sessions
            collection_repository (BaseCollectionRepository):
                repository to work with collection table
            generate_session_name_chain (RunnableSerializable):
                A chain to generate name for the chat session
        """
        self.graph = graph
        self.history_message_repository = history_message_repository
        self.organization_repository = organization_repository
        self.chat_session_repository = chat_session_repository
        self.collection_repository = collection_repository
        self.generate_session_name_chain = generate_session_name_chain

    def chat(
            self,
            messages: List[ChatMessage],
            collection_ids: List[UUID],
            client_context: ClientContext
        ) -> ChatMessage:
        """
        Process a list of chat messages through the agent graph.

        This method:
        1. Converts message formats to LangChain messages
        2. Sets up the initial agent state with messages and empty fields
        3. Runs the agent graph to process the conversation
        4. Extracts the last AI response from the result
        5. Converts it back to the message format

        Args:
            messages (List[ChatMessage]): The chat history and new user input
            collection_ids (List[UUID]): Id of the collection to chat with
            client_context (ClientContext): The authenticated client

        Returns:
            ChatMessage: The AI's response as a ChatMessage

        Raises:
            MessageNotFound: If no AI message is found in the graph output
        """
        # Convert to BaseMessage
        base_messages = convert_to_langchain_messages(messages)

        # Check collection_ids belongs to the client
        if any(
            collection_id not in client_context.collection_ids
            for collection_id in collection_ids
        ):
            raise CollectionNotFound

        # Graph state
        state: AgentState = {
            "organization_id": client_context.organization_id,
            "collection_ids": collection_ids,
            "messages": base_messages,
            "question": None,
            "summary": None,
            "intent": None,
            "rag_docs": None,
            "action_type": None,
            "action_info": None
        }

        # Run graph
        result_state = self.graph.invoke(state)

        # Get result message from AI
        last_ai_message = next(
            (message for message in reversed(result_state["messages"])
            if isinstance(message, AIMessage)), None
        )

        # Check if last AI message exists
        if not last_ai_message:
            raise MessageNotFound()

        return convert_from_langchain_message(last_ai_message)

    def chat_with_session(
            self,
            session_id: UUID,
            input_message: ChatMessage,
            client_context: ClientContext
        ) -> ChatMessage:
        """
        Process a chat message within the context of a specific chat session.

        This method:
        1. Retrieves the conversation history for the given session
        2. Processes the input message in the context of that history
        3. Saves both the input message and AI response to the session history
        4. Returns the AI response


        Args:
            session_id (UUID): The unique identifier of the chat session
            input_message (ChatMessage): The new message from the user
            client_context (ClientContext): The authenticated client

        Returns:
            ChatMessage: The AI's response as a ChatMessage

        Note:
            This method automatically handles persisting the conversation,
            both the user input and AI response, to the session history.
        """
        # Check if chat session exists
        organization_id = client_context.organization_id
        chat_session: Optional[ChatSession] = self.chat_session_repository.get(
            session_id=session_id,
        )
        if not chat_session or chat_session.organization_id != organization_id:
            raise ChatSessionNotFound(session_id)


        # Get history messages
        history_messages: List[HistoryMessage] = self.history_message_repository.get_list(
            session_id,
            organization_id
        )

        # check if no history messages, create name for the session
        if not history_messages:
            session_name = self.generate_session_name_chain.invoke(input_message.content)
            self.chat_session_repository.update(
                session_id=session_id,
                data=ChatSessionUpdateDTO(
                    name=session_name
                )
            )

        # Convert to ChatMessage
        chat_messages: List[ChatMessage] = [ChatMessage(
            type=msg.type,
            content=str(msg.content)
        ) for msg in history_messages]

        # Combine with the current message
        chat_messages.append(input_message)

        # Get result
        collection_ids = [collection.id for collection in chat_session.collections]
        response_message: ChatMessage = self.chat(
            chat_messages,
            collection_ids=collection_ids,
            client_context=client_context
        )

        # Save input message and response message
        self.history_message_repository.create(
            HistoryMessageCreateDTO(
                **input_message.model_dump(),
                session_id=session_id,
                created_at=datetime.now(tz=timezone.utc)
            ),
            organization_id=organization_id
        )

        self.history_message_repository.create(
            HistoryMessageCreateDTO(
                **response_message.model_dump(),
                session_id=session_id,
                created_at=datetime.now(tz=timezone.utc)
            ),
            organization_id=organization_id
        )
        # Return
        return response_message
