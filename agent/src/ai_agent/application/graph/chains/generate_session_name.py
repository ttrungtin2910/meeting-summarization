"""
Chain to generate session chat name
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from ai_agent.infrastructure.language_model import get_language_model

# create prompt template
PROMPT_TEMPLATE = """You are an assistant that summarizes a user message into a \
concise and meaningful conversation title.
Given a message, generate a short, descriptive title (3-7 words) \
that reflects the main topic or intent of the conversation.
Do not include punctuation. Avoid generic titles like "Chat" or "Conversation."

Message: "{user_message}"
Title:
"""

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

# create llm
llm = get_language_model()

# Output parser
parser = StrOutputParser()

# create chain
generate_session_name_chain = prompt | llm | parser
