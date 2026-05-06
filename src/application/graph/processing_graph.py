from langgraph.graph import END, START, StateGraph

from src.application.agents.extractor.agent import extractor_agent
from src.application.agents.orchestrator.agent import orchestrate
from src.application.agents.reader.agent import reader_agent
from src.domain.state import State

graph = StateGraph(State)
graph.add_node("orchestrator", orchestrate)
graph.add_edge(START, "orchestrator")

graph.add_node("reader", reader_agent)
graph.add_node("extractor", extractor_agent)

graph.add_conditional_edges(
    "orchestrator", orchestrate, {"new": "reader", "existing": "comparator"}
)

graph.add_edge("reader", "extractor")

graph.add_node("memory", memory_agent)
graph.add_node("comparator", compare_agent)

graph.add_edge("extractor", "memory")
graph.add_edge("memory", END)

graph.add_conditional_edges(
    "comparator", compare_agent, {"reprocess": "extractor", "discard": END}
)
