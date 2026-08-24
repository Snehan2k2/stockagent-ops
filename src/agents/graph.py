from langgraph.graph import END, START, StateGraph

from src.agents.nodes import (
    critic_node,
    market_expert_node,
    performance_analyst_node,
    report_generator_node,
)
from src.agents.state import AgentState

graph_builder = StateGraph(AgentState)
graph_builder.add_node("performance_analyst", performance_analyst_node)
graph_builder.add_node("market_expert", market_expert_node)
graph_builder.add_node("report_generator", report_generator_node)
graph_builder.add_node("critic", critic_node)

graph_builder.add_edge(START, "performance_analyst")
graph_builder.add_edge("performance_analyst", "market_expert")
graph_builder.add_edge("market_expert", "report_generator")
graph_builder.add_edge("report_generator", "critic")
graph_builder.add_edge("critic", END)

agent_graph = graph_builder.compile()
