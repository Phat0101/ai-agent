import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pycoingecko import CoinGeckoAPI
import redis
from app.core.logging import setup_logger

# Set up logger
logger = setup_logger("crypto_agent")

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Initialize CoinGecko API client
coingecko = CoinGeckoAPI()
logger.info("CoinGecko API client initialized")

# Initialize Redis (if available)
redis_client = None
try:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url)
    redis_client.ping()  # Test the connection
    logger.info(f"Redis client initialized with URL: {redis_url}")
except:
    logger.warning("Redis not available - continuing without caching")

# Initialize Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY is required")

# Initialize LangChain Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=gemini_api_key,
    temperature=0.5,
)
logger.info("Gemini model initialized") 