"""
Chain for generate based on RAG.
"""

from typing import List

from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda

from ai_agent.config import GraphConfig
from ai_agent.infrastructure.dependencies.retriever_dependencies import \
    get_embedding_retriever
from ai_agent.infrastructure.language_model import get_language_model

retriever = get_embedding_retriever()

# Create prompt
system_prompt = f"""You are {GraphConfig.agent_name} of a website:
<<<start of Website content>>>
{GraphConfig.system_description}

You can support the following actions if any (action intent):
{chr(10).join([f"- {name}: {desc}" for name, desc in GraphConfig.actions.items()])}
<<<end of Website content>>>

Respond casually and helpfully to user messages, in markdown format.
"""

HUMAN_PROMPT = """Use the following pieces of retrieved context to answer the question. \

Question: {question}
Context: {context}
Chat History: {history}
Answer:
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", HUMAN_PROMPT)
])

# Create LLM
llm = get_language_model()

def combine_documents(documents: List[Document]) -> str:
    """
    Combine the content of multiple documents into a single string.

    Args:
        documents (List[Document]): List of documents to combine.

    Returns:
        str: Combined text of all documents.
    """
    return '\n'.join([doc.page_content for doc in documents])

# Create chain
generate_rag_chain: Runnable = (
    {
        "history": lambda x: x["history"],
        "question": lambda x: x["question"],
        "context": RunnableLambda(
            lambda x: retriever.invoke(
                x["question"],
                collection_ids=x["collection_ids"],
                organization_id=x["organization_id"]
            )
        ) | combine_documents
    }
    | prompt
    | llm
)
