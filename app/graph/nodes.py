import json
from app.core.config import model, logger
from app.graph.state import (
    CryptoAgentState,
    CryptoReflection,
    CryptoAgentOutput,
    QueryAnalysis,
    ResponseFormat
)
from app.services.coingecko import get_crypto_price, get_historical_price
from app.prompts.templates import QUERY_ANALYSIS_PROMPT, COIN_REFLECTION_PROMPT
from fastapi import HTTPException
from langchain_core.messages import HumanMessage

async def analyze_query(state: CryptoAgentState) -> CryptoAgentState:
    """Analyze the user query to extract coin and query type"""
    logger.info(f"Analyzing query: {state.query}")
    
    # Use structured output for query analysis
    analyzer = model.with_structured_output(QueryAnalysis)
    analysis = analyzer.invoke([HumanMessage(content=QUERY_ANALYSIS_PROMPT.format(query=state.query))])
    logger.info(f"Query analyzed: {analysis}")
    
    if not analysis.coin_id:
        logger.error("No coin_id found in analysis")
        raise HTTPException(status_code=400, detail="Could not identify cryptocurrency in query")
    
    return {
        "coin_id": analysis.coin_id,
        "query_type": analysis.query_type,
        "days": analysis.days,
        "coin_attempts": [analysis.coin_id]
    }

async def fetch_data(state: CryptoAgentState) -> CryptoAgentState:
    """Fetch price or historical data"""
    logger.info(f"Fetching data for coin: {state.coin_id}")
    
    if state.query_type == "price":
        data = await get_crypto_price(state.coin_id)
        logger.info(f"Data fetched: {data}")
        if data:
            return {"current_price": data}
    else:
        data = await get_historical_price(state.coin_id, state.days)
        logger.info(f"Historical data fetched: {data}")
        if data:
            return {"historical_price": data}
    
    return {
        "retry_count": state.retry_count + 1
    }

async def reflect_on_coin(state: CryptoAgentState) -> CryptoAgentState:
    """Reflect on failed data fetch and suggest new coin ID format"""
    logger.info(f"Reflecting on failed attempt for coin: {state.coin_id}")
    
    # Filter out any None values from previous attempts
    valid_attempts = [attempt for attempt in state.coin_attempts if attempt]
    
    # Use structured output for reflection
    reflector = model.with_structured_output(CryptoReflection)
    reflection = reflector.invoke([HumanMessage(content=COIN_REFLECTION_PROMPT.format(
            query=state.query,
            coin_id=state.coin_id,
            attempt_count=state.retry_count,
            previous_attempts=", ".join(valid_attempts)
        ))
    ])
    logger.info(f"Reflection result: {reflection}")
    
    if reflection.sufficient:
        return {"retry_count": 3}
    
    if not reflection.refined_coin_id:
        logger.error("No refined_coin_id provided in reflection")
        return {"retry_count": 3}
    
    return {
        "coin_id": reflection.refined_coin_id,
        "coin_attempts": valid_attempts + [reflection.refined_coin_id]
    }

async def format_response(state: CryptoAgentState) -> CryptoAgentOutput:
    """Format the final response"""
    logger.info("Formatting final response")
    
    formatter = model.with_structured_output(ResponseFormat)
    
    if state.current_price:
        price_data = state.current_price[state.coin_id]
        context = {
            "query": state.query,
            "coin": state.coin_id,
            "price": price_data["usd"],
            "change_24h": price_data.get("usd_24h_change", 0),
            "market_cap": price_data.get("usd_market_cap", 0)
        }
        response = formatter.invoke(
            [HumanMessage(content=f"Format a response for the query: {state.query}\nPrice data: {json.dumps(context)}")]
        )
        return {
            "result": response.result,
            "data": state.current_price
        }
    elif state.historical_price:
        context = {
            "query": state.query,
            "coin": state.coin_id,
            "days": state.days,
            "data_points": len(state.historical_price["prices"]),
            "price_range": {
                "start": state.historical_price["prices"][0][1],
                "end": state.historical_price["prices"][-1][1]
            }
        }
        response = formatter.invoke(
            [HumanMessage(content=f"Format a response for the query: {state.query}\nHistorical data: {json.dumps(context)}")]
        )
        return {
            "result": response.result,
            "data": state.historical_price
        }
    else:
        error_msg = f"Could not fetch data for {state.coin_id} after {state.retry_count} attempts"
        logger.error(error_msg)
        return {
            "result": f"Could not fetch data for {state.coin_id} after {state.retry_count} attempts, please try different coin",
            "data": {}
        }