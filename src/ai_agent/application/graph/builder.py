"""
Builder module for constructing the agent workflow graph.
"""

from langgraph.graph import END, StateGraph

from ai_agent.application.graph.nodes import (detect_intent, generate_chitchat,
                                              generate_rag, invalid,
                                              out_of_scope, rephrase,
                                              summarize)
from ai_agent.application.graph.state import AgentState
from ai_agent.config import GraphConfig

# Initialize the graph
workflow = StateGraph(AgentState)

# add nodes
workflow.add_node(GraphConfig.nodes["DETECT_INTENT"], detect_intent)
workflow.add_node(GraphConfig.nodes["GENERATE_CHITCHAT"], generate_chitchat)
workflow.add_node(GraphConfig.nodes["GENERATE_RAG"], generate_rag)
workflow.add_node(GraphConfig.nodes["INVALID"], invalid)
workflow.add_node(GraphConfig.nodes["OUT_OF_SCOPE"], out_of_scope)
workflow.add_node(GraphConfig.nodes["REPHRASE"], rephrase)
workflow.add_node(GraphConfig.nodes["SUMMARIZE"], summarize)

workflow.set_entry_point(GraphConfig.nodes["SUMMARIZE"])

# add edges
def intent_route(state: AgentState) -> str:
    """
    Determine the next node in the graph based on the detected user intent.

    Args:
        state (AgentState): The current state of the agent, containing messages and intent.

    Returns:
        str: The name of the next node to route to, depending on the detected intent.
             - "chitchat"   -> GENERATE_CHITCHAT (LLM-based answer)
             - "rag"        -> GENERATE_RAG (retrieve documents for RAG)
             - "out_of_scope" -> OUT_OF_SCOPE (unsupported query)
             - "invalid"    -> INVALID (input doesn't match expected structure)
             - "action"     -> (add later)
    """
    intent = state["intent"]
    if intent == "chitchat":
        return GraphConfig.nodes["GENERATE_CHITCHAT"]
    if intent == "rag":
        return GraphConfig.nodes["GENERATE_RAG"]
    if intent == "out_of_scope":
        return GraphConfig.nodes["GENERATE_RAG"]
    if intent == "invalid":
        return GraphConfig.nodes["INVALID"]

    # Placeholder for future actions
    if intent == "action":
        pass

    return GraphConfig.nodes["INVALID"]

# Add conditional routing
workflow.add_conditional_edges(
    GraphConfig.nodes["DETECT_INTENT"],
    intent_route
)

# Add static edges
workflow.add_edge(GraphConfig.nodes["SUMMARIZE"], GraphConfig.nodes["REPHRASE"])
workflow.add_edge(GraphConfig.nodes["REPHRASE"], GraphConfig.nodes["DETECT_INTENT"])
workflow.add_edge(GraphConfig.nodes["GENERATE_CHITCHAT"], END)
workflow.add_edge(GraphConfig.nodes["OUT_OF_SCOPE"], END)
workflow.add_edge(GraphConfig.nodes["INVALID"], END)
workflow.add_edge(GraphConfig.nodes["GENERATE_RAG"], END)

app = workflow.compile()

if __name__ == "__main__":
    print(app.get_graph().draw_mermaid())
