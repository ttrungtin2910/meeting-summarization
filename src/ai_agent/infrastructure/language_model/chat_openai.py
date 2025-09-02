"""
Language model implementation for OpenAI's Chat API.

Defines the ChatOpenAIModel class to initialize and return a ChatOpenAI instance
based on the provided configuration.
"""

from langchain_openai import ChatOpenAI

from .base import BaseLanguageModel


class ChatOpenAIModel(BaseLanguageModel):
    """
    Language model implementation for OpenAI service.
    It inherits from BaseLanguageModel and implements the get_model() method to return an instance of ChatOpenAI.
    """

    def __init__(self, config):
        """
        Initialize the ChatOpenAI model using the provided configuration.

        Args:
            config (dict): Dictionary containing required keys:
                - "API_KEY"
                - "MODEL"
                - "TEMPERATURE"
        """

        self.api_key = config.get("API_KEY")
        self.model = config.get("MODEL")
        self.temperature = config.get("TEMPERATURE")

    def get_model(self) -> ChatOpenAI:
        """
        Return an instance of ChatOpenAI with the current configuration.

        Returns:
            ChatOpenAI: An initialized instance of ChatOpenAI model.
        """

        return ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
        )
