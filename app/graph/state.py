from dataclasses import dataclass, field
from typing import List, Optional, Dict, TypedDict, Literal
from pydantic import BaseModel, Field

class ResponseFormat(BaseModel):
    """Structured output for response formatting"""
    result: str = Field(description="Natural language response describing the price/historical data")

class QueryAnalysis(BaseModel):
    """Structured output for query analysis"""
    coin_id: str = Field(description="The CoinGecko ID of the cryptocurrency (lowercase)")
    query_type: Literal["price", "historical"] = Field(description="Type of query (price or historical)")
    days: Optional[int] = Field(description="Number of days for historical data", default=None)

class CryptoReflection(BaseModel):
    """Reflection on failed coin ID attempts"""
    refined_coin_id: str = Field(description="Refined coin ID to try next")
    sufficient: bool = Field(description="Whether we should stop trying to refine the coin ID")
    reasoning: str = Field(description="Reasoning behind the refinement or decision to stop")

@dataclass(kw_only=True)
class CryptoAgentState:
    """State for the crypto agent workflow"""
    query: str = field(default="")
    coin_id: str = field(default="")
    query_type: Literal["price", "historical"] = field(default="price")
    days: Optional[int] = field(default=None)
    current_price: Optional[Dict] = field(default=None)
    historical_price: Optional[Dict] = field(default=None)
    coin_attempts: List[str] = field(default_factory=list)
    retry_count: int = field(default=0)

class CryptoAgentInput(TypedDict):
    query: str

class CryptoAgentOutput(TypedDict):
    result: str
    data: Dict 