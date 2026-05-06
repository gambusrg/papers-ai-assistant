from functools import partial

from langgraph.graph import END, START, StateGraph

from src.application.agents.conversational.agent import (
    conversation_agent,
    decide_routing,
)
from src.core.dependency_injector import llm, vector_store
from src.domain.conversation_state import ConversationState

graph = StateGraph(ConversationState)
graph.add_node("conversational", partial(conversation_agent, llm=llm))
graph.add_edge(START, "conversational")

graph.add_conditional_edges(
    "conversational", decide_routing, {"search": END, "end": END}
)
