from typing import Literal
from langgraph.graph import StateGraph, END
from app.graph.state import CryptoAgentState, CryptoAgentInput, CryptoAgentOutput
from app.graph.nodes import analyze_query, fetch_data, reflect_on_coin, format_response
from app.core.config import logger

def should_retry(state: CryptoAgentState) -> Literal["reflect", "format_response"]:
    """Determine if we should try another coin ID format"""
    if state.retry_count < 3 and not (state.current_price or state.historical_price):
        return "reflect"
    return "format_response"

def create_workflow() -> StateGraph:
    """Create and configure the workflow graph"""
    # Create the graph
    workflow = StateGraph(CryptoAgentState, input=CryptoAgentInput, output=CryptoAgentOutput)

    # Add nodes
    workflow.add_node("analyze_query", analyze_query)
    workflow.add_node("fetch_data", fetch_data)
    workflow.add_node("reflect", reflect_on_coin)
    workflow.add_node("format_response", format_response)

    # Connect nodes
    workflow.set_entry_point("analyze_query")
    workflow.add_edge("analyze_query", "fetch_data")
    workflow.add_conditional_edges(
        "fetch_data",
        should_retry,
        {
            "reflect": "reflect",
            "format_response": "format_response"
        }
    )
    workflow.add_edge("reflect", "fetch_data")
    workflow.add_edge("format_response", END)

    # Compile the graph
    graph = workflow.compile()
    logger.info("Workflow graph compiled")
    
    return graph 