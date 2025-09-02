"""
Concrete language model implementation for Azure OpenAI service.

Defines the AzureChatOpenAIModel class to initialize and return an AzureChatOpenAI instance
based on provided configuration settings.
"""

from langchain_openai import AzureChatOpenAI

from .base import BaseLanguageModel


class AzureChatOpenAIModel(BaseLanguageModel):
    """
    Language model implementation for Azure OpenAI service.
    It inherits from BaseLanguageModel and implements the get_model() method
    to return an instance of AzureChatOpenAI.
    """
    def __init__(self, config):
        """
        Initialize the model configuration for connecting to the Azure/OpenAI service.

        Args:
            config: A configuration object that must provide the following attributes:
                - api_key (str): The API key used to authenticate with the service.
                - api_endpoint (str): The endpoint URL of the Azure/OpenAI service.
                - api_version (str): The version of the API to use.
                - model (str): The name or deployment ID of the model to use.
                - temperature (float): The temperature setting for model response variability.
        """
        self.api_key = config.api_key
        self.api_endpoint = config.api_endpoint
        self.api_version = config.api_version
        self.model = config.model
        self.temperature = config.temperature

    def get_model(self) -> AzureChatOpenAI:
        """
        Return an instance of AzureChatOpenAI with the current configuration.

        Returns:
            AzureChatOpenAI: An initialized instance of Azure's ChatOpenAI model.
        """
        return AzureChatOpenAI(
            azure_endpoint=self.api_endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
            azure_deployment=self.model,
            temperature=self.temperature,
        )
