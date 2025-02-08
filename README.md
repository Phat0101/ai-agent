# Crypto Price AI Agent

# Main application description
An intelligent agent built with LangGraph and FastAPI that provides cryptocurrency price information using the CoinGecko API. The agent can understand natural language queries and provide both current and historical price data with automatic retry and refinement capabilities.

## Features

# Core capabilities of the application
- 🤖 Natural language query understanding using Google's Gemini AI
- 💰 Real-time cryptocurrency price data from CoinGecko API
- 📈 Historical price data support with interactive charts
- 🔄 Automatic retry with query refinement
- 💾 Redis caching for improved performance
- 📝 Comprehensive logging system
- 🚀 FastAPI backend with rate limiting
- 🎯 Streamlit frontend for easy interaction

## Project Structure

# Directory structure with explanations
```
.
├── app/                      # Main application directory
│   ├── core/                # Configuration and logging
│   │   ├── config.py        # Service configuration and initialization
│   │   └── logging.py       # Logging setup
│   ├── graph/               # LangGraph workflow components
│   │   ├── nodes.py         # Graph nodes for query processing
│   │   ├── state.py         # State management definitions
│   │   └── workflow.py      # Workflow graph 
│   ├── services/            # External service integrations
│   │   ├── coingecko.py     # CoinGecko API client
│   └── prompts/             # AI model prompts
│       └── templates.py      # Prompt templates for AI
├── main.py                   # FastAPI application entry point
├── streamlit_app.py          # Streamlit frontend application
└── requirements.txt          # Project dependencies
```

## Prerequisites

# Required components before installation
- Python 3.9+
- Redis (optional, for caching)
- Google Gemini API key

### Redis Setup

# Platform-specific Redis installation instructions
#### macOS
Using Homebrew:
```bash
# Install Redis
brew install redis

# Start Redis
brew services start redis

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

#### Linux (Ubuntu/Debian)
```bash
# Install Redis
sudo apt update
sudo apt install redis-server

# Start Redis and enable auto-start
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

#### Windows
1. Using Windows Subsystem for Linux (WSL) - Recommended:
```bash
# Install WSL if not already installed
wsl --install

# Follow Linux instructions above in WSL
```

2. Using Windows native installation:
   - Download the latest Redis release for Windows from [GitHub](https://github.com/microsoftarchive/redis/releases)
   - Run the installer (Redis-x64-xxx.msi)
   - Redis will be installed as a Windows service and start automatically

#### Docker (Cross-platform)
```bash
# Pull and run Redis container
docker run --name redis -d -p 6379:6379 redis
```

## Installation

# Step-by-step installation process
1. Clone the repository:
```bash
git clone <repository-url>
cd crypto-price-ai-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_URL=redis://localhost:6379  # Optional, for caching
```

## Running the Application

### Standard Deployment
# Instructions for starting both backend and frontend
1. Start the FastAPI backend:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run streamlit_app.py
```
The web interface will be available at `http://localhost:8501`

### Docker Deployment
# Instructions for running with Docker
1. Make sure you have Docker and Docker Compose installed on your system.

2. Create a `.env` file in the project root with your configuration:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Build and start the containers:
```bash
docker-compose up --build
```

This will start three containers:
- Frontend (Streamlit): http://localhost:8501
- Backend (FastAPI): http://localhost:8000
- Redis: localhost:6379

#### Useful Docker Commands
```bash
# Start the services in detached mode
docker-compose up -d

# View logs of all services
docker-compose logs -f

# View logs of a specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis

# Stop the services
docker-compose down

# Stop the services and remove volumes
docker-compose down -v

# Rebuild a specific service
docker-compose up --build backend
```

#### Container Structure
The application is containerized into three services:
1. **Backend (FastAPI)**
   - Handles API requests
   - Processes queries using Gemini AI
   - Communicates with CoinGecko API
   - Caches responses in Redis

2. **Frontend (Streamlit)**
   - Provides user interface
   - Displays real-time cryptocurrency data
   - Shows interactive charts
   - Communicates with backend API

3. **Redis**
   - Caches API responses
   - Improves response times
   - Reduces external API calls
   - Persists data using volumes

#### Docker Volumes
- `redis_data`: Persists Redis data between container restarts

#### Networks
- `crypto_network`: Internal network for service communication

## Using the Application

### Web Interface
1. Open your browser and navigate to `http://localhost:8501`
2. Enter your query in the text input field
3. View the response, including:
   - Natural language response
   - Interactive price charts (for historical queries)
   - Raw data in expandable section

### API Endpoints

# Available API endpoints and usage
#### Query Endpoint
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the price of Bitcoin?"}'
```

#### Health Check
```bash
curl "http://localhost:8000/health"
```

### Example Queries
- Current price: "What is the price of Bitcoin?"
- Historical data: "Show me Ethereum's price history for the last 7 days"
- Alternative names: "What's the current price of DOGE?"

## Features

### Backend (FastAPI)
# Backend capabilities
- Natural language processing with Gemini AI
- Automatic query refinement
- Redis caching for improved performance
- Rate limiting (5 requests/minute per IP)
- Comprehensive error handling
- Health check endpoint

### Frontend (Streamlit)
# Frontend features
- Clean, modern interface
- Real-time API status monitoring
- Interactive price charts
- Query examples
- Raw data viewer
- Error handling and user feedback

## Error Handling

# Comprehensive error handling capabilities
The system includes comprehensive error handling:
- Invalid cryptocurrency names
- API rate limits and failures
- Cache failures
- Query parsing errors
- Network connectivity issues

## Logging

# Logging system configuration
Logs are stored in `logs/crypto_agent.log` with:
- Rotating file handler (10MB max size)
- Console output
- Detailed cache operations logging
- API call tracking
- Error tracing

## License

MIT License

## Acknowledgments

# Credits and references
- [LangGraph](https://github.com/langchain-ai/langgraph) for the workflow framework
- [CoinGecko](https://www.coingecko.com/en/api) for the cryptocurrency data API
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Streamlit](https://streamlit.io/) for the frontend interface
- [Google Gemini](https://ai.google.dev/) for natural language processing

## Author

Patrick Nguyen