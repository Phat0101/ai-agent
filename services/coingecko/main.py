from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pycoingecko import CoinGeckoAPI
import redis
import json
import os
import logging
import socket
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Get container hostname for identification
HOSTNAME = socket.gethostname()

# Configure logging
logger = logging.getLogger("coingecko_service")
logger.setLevel(logging.INFO)

# Create formatters with hostname
file_formatter = logging.Formatter(
    f'%(asctime)s - [Container: {HOSTNAME}] - %(name)s - %(levelname)s - %(message)s'
)
console_formatter = logging.Formatter(
    f'%(asctime)s - [Container: {HOSTNAME}] - %(levelname)s - %(message)s'
)

# File handler (rotating file handler)
file_handler = RotatingFileHandler(
    'logs/coingecko_service.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Load environment variables
load_dotenv()

# Get port from environment variable
PORT = int(os.getenv("PORT", 8001))

# Initialize FastAPI app
app = FastAPI(
    title="CoinGecko Service",
    description="Microservice for CoinGecko API interactions with caching",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CoinGecko API client
coingecko = CoinGeckoAPI()

# Initialize Redis
redis_client = None
try:
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    redis_client = redis.from_url(redis_url)
    redis_client.ping()
except:
    print("Redis not available - continuing without caching")

@app.get("/health")
async def health_check():
    """Health check endpoint with container identification."""
    return {
        "status": "healthy",
        "container": HOSTNAME
    }

@app.get("/price/{coin_id}")
async def get_crypto_price(coin_id: str):
    """Get current price for a cryptocurrency."""
    try:
        logger.info(f"[Container: {HOSTNAME}] Processing price request for coin_id: {coin_id}")
        
        if redis_client:
            cache_key = f"price:{coin_id}"
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"[Container: {HOSTNAME}] ✅ Cache HIT for price data - coin_id: {coin_id}")
                return json.loads(cached_data)
            
            logger.info(f"[Container: {HOSTNAME}] ❌ Cache MISS for price data - coin_id: {coin_id}")
        
        logger.info(f"[Container: {HOSTNAME}] Fetching price data from CoinGecko API - coin_id: {coin_id}")
        data = coingecko.get_price(
            ids=coin_id,
            vs_currencies='usd',
            include_market_cap=True,
            include_24hr_change=True
        )
        
        if not data:
            logger.error(f"[Container: {HOSTNAME}] No data found for coin_id: {coin_id}")
            raise HTTPException(status_code=404, detail=f"No data found for coin: {coin_id}")
            
        if redis_client:
            redis_client.setex(cache_key, 60, json.dumps(data))
            logger.info(f"[Container: {HOSTNAME}] Cached price data for coin_id: {coin_id}")
            
        return data
    except Exception as e:
        logger.error(f"[Container: {HOSTNAME}] Error fetching price for {coin_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historical/{coin_id}")
async def get_historical_price(coin_id: str, days: int):
    """Get historical price data."""
    try:
        if redis_client:
            cache_key = f"historical:{coin_id}:{days}"
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"✅ Cache HIT for historical data - coin_id: {coin_id}, days: {days}")
                return json.loads(cached_data)
            
            logger.info(f"❌ Cache MISS for historical data - coin_id: {coin_id}, days: {days}")
        
        logger.info(f"Fetching historical data from CoinGecko API - coin_id: {coin_id}, days: {days}")
        data = coingecko.get_coin_market_chart_by_id(
            id=coin_id,
            vs_currency='usd',
            days=days
        )
        
        if not data:
            logger.error(f"No historical data found for coin_id: {coin_id}")
            raise HTTPException(status_code=404, detail=f"No historical data found for coin: {coin_id}")
            
        if redis_client:
            redis_client.setex(cache_key, 60, json.dumps(data))
            logger.info(f"Cached historical data for coin_id: {coin_id}, days: {days}")
            
        return data
    except Exception as e:
        logger.error(f"Error fetching historical data for {coin_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT) 