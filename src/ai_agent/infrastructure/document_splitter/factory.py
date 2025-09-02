"""
Factory module for document splitters.

Provides a function to initialize and return a configured DocumentSplitter
based on the provider specified in the SplitterConfig.
"""


from ai_agent.config import SplitterConfig

from .recursive_character_text_splitter import RecursiveSplitter


def get_splitter():
    """
    Factory function to initialize and return the configured Document splitter.

    This function reads the provider from `SplitterConfig.PROVIDER` and
    initializes the corresponding splitter.

    Returns:
        An instance of the selected splitter class.

    Raises:
        ValueError: If the specified provider in SplitterConfig.PROVIDER is not supported.
    """
    provider = SplitterConfig.provider.lower()
    if provider == "recursive_character_text_splitter":
        return RecursiveSplitter(SplitterConfig)
    raise ValueError(f"Unsupported splitter provider: {SplitterConfig.provider}")
