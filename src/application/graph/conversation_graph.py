from langgraph.graph import END, START, StateGraph

from src.application.agents.conversational.agent import (
    conversation_agent,
    decide_routing,
)
from src.application.agents.memory.agent import memory_agent
from src.domain.conversation_state import ConversationState

graph = StateGraph(ConversationState)
graph.add_node("conversational", conversation_agent)
graph.add_edge(START, "conversational")

graph.add_node("memory", memory_agent)

graph.add_conditional_edges(
    "conversational", decide_routing, {"search": "memory", "end": END}
)

graph.add_edge("memory", "conversational")
