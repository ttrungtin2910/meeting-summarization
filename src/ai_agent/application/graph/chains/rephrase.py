"""
Chain for rephrase the question based on summary.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from ai_agent.infrastructure.language_model import get_language_model

# Create prompt
PROMPT_TEMPLATE = """Given the following conversation and a follow up message, \
rephrase the follow up message to a meaningful standalone message.
If the follow up message is empty, clearly gibberish, such as repeated letters, \
random characters, or has no recognizable words, return it as-is without modification.
The message could be interpreted as a real message or reaction in conversation, \
even if it's short or vague (e.g., "how", "what?", "?", "...?", "ok?")
Only return the content of the standalone message, in the same language with the follow up message.
<<<Chat Summary>>>
{summary}

<<<Follow Up message>>>{question}

<<<Standalone message>>>"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# Create LLM
llm = get_language_model()

# Parser
parser = StrOutputParser()

# Create chain
rephrase_chain = prompt | llm | parser
