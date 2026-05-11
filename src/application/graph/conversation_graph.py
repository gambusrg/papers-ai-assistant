from functools import partial

from langgraph.graph import END, START, StateGraph

from src.application.agents.conversational.agent import (
    conversation_agent,
    decide_routing,
)
from src.core.dependency_injector import llm, vector_store
from src.domain.conversation_state import ConversationState

conversation_graph = StateGraph(ConversationState)
conversation_graph.add_node("conversational", partial(conversation_agent, llm=llm))
conversation_graph.add_edge(START, "conversational")

conversation_graph.add_conditional_edges(
    "conversational", decide_routing, {"search": END, "end": END}
)
conversation_graph = conversation_graph.compile()
