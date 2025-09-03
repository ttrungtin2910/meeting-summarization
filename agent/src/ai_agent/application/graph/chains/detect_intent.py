"""
Chain for detecting user intent based on conversation input.
"""

from langchain_core.prompts import ChatPromptTemplate

from ai_agent.application.graph.models.intent import DetectIntentOutput
from ai_agent.config import GraphConfig
from ai_agent.infrastructure.language_model import get_language_model

# Create prompt
system_prompt = f"""You are {GraphConfig.agent_name} of a website:
<<<start of Website content>>>
{GraphConfig.system_description}

You can support the following actions if any (action intent):
{chr(10).join([f"- {name}: {desc}" for name, desc in GraphConfig.actions.items()]) or "Empty action"}
<<<end of Website content>>>

Classify the user message into one of these intents:
- chitchat: Friendly greetings, or casual questions related to the assistant \
or the user expresses gratitude after the conversation \
like "hello", "how are you", "what's your name", "What can you do"
- rag: Any question that is related to the website, \
its functionality, features, usage, product offering, or user experience. \
If you think the message is relevant and may require information stored in documentation \
or product knowledge, assign it to this category
- action
- out_of_scope: Questions out of the scope of the <<<Website content>>>, like about weather, politics.
- invalid: input is empty, nonsensical, gibberish, or looks like spam
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}")
    ]
)

# Create llm
llm = get_language_model().with_structured_output(DetectIntentOutput)

# Create chain
detect_intent_chain = prompt | llm
