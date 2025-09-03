"""
Chain for generate chitchat.
"""

from langchain_core.prompts import ChatPromptTemplate

from ai_agent.config import GraphConfig
from ai_agent.infrastructure.language_model import get_language_model

# create prompt
system_prompt = f"""You are {GraphConfig.agent_name} of a website:
<<<start of Website content>>>
{GraphConfig.system_description}

You can support the following actions if any (action intent):
{chr(10).join([f"- {name}: {desc}" for name, desc in GraphConfig.actions.items()])}
<<<end of Website content>>>

Respond casually and helpfully to user messages, in markdown format.
"""

HUMAN_PROMPT = """Response to user message:
Current question: {question}
Chat History so far: {summary}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", HUMAN_PROMPT)
])

# create llm
llm = get_language_model()

# create chain
generate_chitchat_chain = prompt | llm
