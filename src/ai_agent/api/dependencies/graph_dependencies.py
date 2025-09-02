"""
Graph dependencies module providing factory functions for the agent graph.
"""

from langgraph.graph.state import CompiledStateGraph

from ai_agent.application.graph.builder import app


def get_graph() -> CompiledStateGraph:
    """
    Factory function that provides the compiled agent graph.

    Returns:
        CompiledStateGraph: The compiled agent graph for processing conversations
    """
    return app
