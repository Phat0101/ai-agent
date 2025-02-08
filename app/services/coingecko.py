import json
from app.core.config import coingecko, redis_client, logger

async def get_crypto_price(coin_id: str) -> dict:
    """Get current price for a cryptocurrency."""
    logger.info(f"Fetching price for coin: {coin_id}")
    
    if redis_client:
        cache_key = f"price:{coin_id}"
        logger.info(f"Checking Redis cache for key: {cache_key}")
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            logger.info(f"✨ Cache HIT: Retrieved price for {coin_id} from Redis cache")
            return json.loads(cached_data)
        logger.info(f"❌ Cache MISS for {coin_id} - fetching from CoinGecko API")
    else:
        logger.info("Redis not available - fetching directly from CoinGecko API")
    
    try:
        logger.info(f"Making API call to CoinGecko for {coin_id}")
        data = coingecko.get_price(ids=coin_id, vs_currencies='usd', 
                                include_market_cap=True, 
                                include_24hr_change=True)
        if not data:
            logger.warning(f"No data returned for coin: {coin_id}")
            return None
            
        if redis_client:
            logger.info(f"Caching price data for {coin_id} in Redis (TTL: 60s)")
            redis_client.setex(cache_key, 60, json.dumps(data))  # Cache for 60 seconds
            
        return data
    except Exception as e:
        logger.error(f"Error fetching price for {coin_id}: {str(e)}")
        return None

async def get_historical_price(coin_id: str, days: int) -> dict:
    """Get historical price data."""
    logger.info(f"Fetching historical data for coin: {coin_id}, days: {days}")
    
    if redis_client:
        cache_key = f"historical:{coin_id}:{days}"
        logger.info(f"Checking Redis cache for key: {cache_key}")
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            logger.info(f"✨ Cache HIT: Retrieved historical data for {coin_id} from Redis cache")
            return json.loads(cached_data)
        logger.info(f"❌ Cache MISS for {coin_id} historical data - fetching from CoinGecko API")
    else:
        logger.info("Redis not available - fetching directly from CoinGecko API")
    
    try:
        logger.info(f"Making API call to CoinGecko for {coin_id} historical data")
        data = coingecko.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=days)
        if not data:
            logger.warning(f"No historical data returned for coin: {coin_id}")
            return None
            
        if redis_client:
            logger.info(f"Caching historical data for {coin_id} in Redis (TTL: 60s)")
            redis_client.setex(cache_key, 60, json.dumps(data))  # Cache for 60 seconds
            
        return data
    except Exception as e:
        logger.error(f"Error fetching historical data for {coin_id}: {str(e)}")
        return None 