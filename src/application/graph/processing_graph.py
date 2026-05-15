from functools import partial

from langgraph.graph import END, START, StateGraph

from src.application.agents.comparator.agent import compare, comparator_node
from src.application.agents.extractor.agent import extractor_agent
from src.application.agents.indexer.agent import indexer_agent
from src.application.agents.memory.agent import memory_agent
from src.application.agents.orchestrator.agent import orchestrate
from src.application.agents.reader.agent import reader_agent
from src.core.dependency_injector import llm, vector_store, conversation_repo
from src.domain.state import State

graph = StateGraph(State)

graph.add_conditional_edges(
    START,
    partial(orchestrate, vector_store=vector_store),
    {"new": "reader", "existing": "comparator"},
)

graph.add_node("reader", reader_agent)
graph.add_node("indexer", partial(indexer_agent, vector_store=vector_store))
graph.add_node(
    "extractor", partial(extractor_agent, llm=llm, vector_store=vector_store)
)

graph.add_edge("reader", "indexer")
graph.add_edge("indexer", "extractor")

graph.add_node("memory", partial(memory_agent, vector_store=vector_store, sql=conversation_repo))

graph.add_edge("extractor", "memory")
graph.add_edge("memory", END)

graph.add_node("comparator", comparator_node)
graph.add_conditional_edges(
    "comparator", compare, {"reprocess": "extractor", "discard": END}
)
graph = graph.compile()
