"""
Factory module for initializing language models.

Provides a function to select and return a language model instance
(e.g., ChatOpenAI, AzureChatOpenAI) based on the configured provider.
"""

from ai_agent.config import LLMConfig

from .azure_chat_openai import AzureChatOpenAIModel
from .chat_openai import ChatOpenAIModel


def get_language_model():
    """
    Factory function that returns the actual language model instance (ChatOpenAI)
    based on the configured provider.

    Returns:
        BaseLanguageModel: An instance of a chat model (e.g., ChatOpenAI)
    """

    provider = LLMConfig.provider.lower()

    if provider == "azure":
        model_instance = AzureChatOpenAIModel(LLMConfig)
        return model_instance.get_model()

    if provider == "openai":
        model_instance = ChatOpenAIModel(LLMConfig)
        return model_instance.get_model()

    raise ValueError(f"Unsupported language model provider: {LLMConfig.provider}")
