"""
Chain for summarize the chat history.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda

from ai_agent.application.graph.helpers.message_helper import format_messages
from ai_agent.infrastructure.language_model import get_language_model

# Create prompt
HUMAN_MESSAGE = """Given the following conversation between a user and an AI assistant, \
generate a summary of the discussion.

Conversation:
{messages}

Summary:"""

prompt = ChatPromptTemplate.from_messages(
    ("human", HUMAN_MESSAGE)
    )

# Create LLM
llm = get_language_model()

# Parser
parser = StrOutputParser()

# Create chain
summarize_chain: Runnable =  {"messages": RunnableLambda(format_messages)} | prompt | llm | parser
