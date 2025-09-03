"""
Defines the state for managing data flow between nodes in the agent graph.
"""

from typing import Annotated, List, Optional, TypedDict
from uuid import UUID

from langchain.schema import Document
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):
    """
    Represents the state passed between nodes in the agent flow.

    Attributes:
        organization_id: ID of the organization

        collection_ids: IDs of the collections, used to retrieve documents for RAG

        messages: Full message history exchanged between the user and assistant.
                  Must be a list of LangChain BaseMessage objects (e.g., HumanMessage, AIMessage).

        question: rephrase from the list of messages

        summary: summary generated from list of messages

        intent: The detected high-level intent of the current user message.
                Should be one of: "chitchat", "rag", "action", "out_of_scope", or "invalid".

        rag_docs: The retrieved documents relevant to the user query,
                  used in the RAG (Retrieval-Augmented Generation) pipeline.

        action_type: (Optional) Type of action to be executed, if intent is "action".
                     For example: "create_parsing_rule", etc.

        action_info: (Optional) Dictionary storing information collected from the user
                     needed to execute the action. Populated during interactive steps.
    """
    organization_id: UUID
    collection_ids: List[UUID]
    messages: Annotated[List[BaseMessage], add_messages]
    question: Optional[str]
    summary: Optional[str]
    intent: Optional[str]
    rag_docs: Optional[List[Document]]

    # For future action-related flow
    action_type: Optional[str]
    action_info: Optional[dict]
