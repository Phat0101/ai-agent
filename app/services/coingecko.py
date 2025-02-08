import json
import os
import httpx
from app.core.config import logger

# Use service name for Docker's internal DNS resolution
COINGECKO_SERVICE_URL = os.getenv("COINGECKO_SERVICE_URL", "http://coingecko:8001")

async def get_crypto_price(coin_id: str) -> dict:
    """Get current price for a cryptocurrency."""
    logger.info(f"Fetching price for coin: {coin_id}")
    
    try:
        async with httpx.AsyncClient() as client:
            # Docker's internal DNS will handle load balancing
            response = await client.get(f"{COINGECKO_SERVICE_URL}/price/{coin_id}", timeout=10.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching price for {coin_id}: {str(e)}")
        return None

async def get_historical_price(coin_id: str, days: int) -> dict:
    """Get historical price data."""
    logger.info(f"Fetching historical data for coin: {coin_id}, days: {days}")
    
    try:
        async with httpx.AsyncClient() as client:
            # Docker's internal DNS will handle load balancing
            response = await client.get(
                f"{COINGECKO_SERVICE_URL}/historical/{coin_id}",
                params={"days": days},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching historical data for {coin_id}: {str(e)}")
        return None 