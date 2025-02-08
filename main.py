from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import logger
from app.graph.state import CryptoAgentState
from app.graph.workflow import create_workflow

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Crypto Price AI Agent",
    description="An AI agent that provides cryptocurrency price information using CoinGecko API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class Query(BaseModel):
    query: str

# Create the workflow graph
graph = create_workflow()

# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."}
    )

@app.post("/query")
@limiter.limit("5/minute")  # Rate limit: 5 requests per minute per IP
async def process_query(request: Request, query: Query):
    try:
        logger.info(f"Received query: {query.query}")
        
        # Input validation
        if not query.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        # Initialize the state
        state = CryptoAgentState(query=query.query)
        
        # Run the graph
        logger.info("Executing workflow")
        final_output = await graph.ainvoke({"query": query.query})
        logger.info(f"Workflow completed: {final_output}")
        
        return final_output
            
    except HTTPException as e:
        # Re-raise HTTP exceptions to be handled by the exception handler
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request"
        )

# Health check endpoint
@app.get("/health")
@limiter.limit("10/minute")  # Higher rate limit for health checks
async def health_check(request: Request):
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server")
    uvicorn.run(app, host="0.0.0.0", port=8000) 