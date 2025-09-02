"""
LLM chain dependencies modules.
"""

from ai_agent.application.graph.chains.generate_session_name import \
    generate_session_name_chain


def get_generate_session_name_chain():
    """
    Factory function that provides access to the session name generation chain.

    Returns:
        LLMChain: The chain configured to generate appropriate session names
    """
    return generate_session_name_chain