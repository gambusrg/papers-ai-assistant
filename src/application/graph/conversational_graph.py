from functools import partial

from langgraph.graph import END, START, StateGraph

from src.application.agents.common.router import route
from src.application.agents.conversational.agent import generator_node, rag_node
from src.core.dependency_injector import conversation_repo, llm, vector_store
from src.domain.state import ConversationState

graph = StateGraph(ConversationState)

graph.add_node("rag", partial(rag_node, vector_store=vector_store))
graph.add_node("generator", partial(generator_node, llm=llm, sql=conversation_repo))

graph.add_conditional_edges(
    START, partial(route, llm=llm), {"rag": "rag", "chat": "generator"}
)
graph.add_edge("rag", "generator")
graph.add_edge("generator", END)

conv_graph = graph.compile()
