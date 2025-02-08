# Crypto Price AI Agent

# Main application description
An intelligent agent built with LangGraph and FastAPI that provides cryptocurrency price information using a microservices architecture. The system consists of multiple services that work together to process natural language queries and provide real-time cryptocurrency data.

## 🏗 Architecture Overview

The application is structured as a microservices-based system with the following components:

### System Architecture

```mermaid
graph TD
    User[User] --> Frontend[Frontend Service]
    Frontend --> Backend[Main Backend Service]
    
    subgraph LangGraph Workflow
        QueryAnalysis[Query Analysis Node]
        FetchData[Data Fetch Node]
        Reflection[Reflection Node]
        FormatResponse[Response Format Node]
        
        QueryAnalysis --> FetchData
        FetchData --> Reflection
        Reflection --> FetchData
        FetchData --> FormatResponse
    end
    
    Backend --> QueryAnalysis
    FormatResponse --> Frontend
    
    subgraph CoinGecko Services
        CoinGecko1[CoinGecko Service 1]
        CoinGecko2[CoinGecko Service 2]
        CoinGecko3[CoinGecko Service 3]
    end
    
    FetchData --> CoinGecko1
    FetchData --> CoinGecko2
    FetchData --> CoinGecko3
    
    CoinGecko1 --> Redis[(Redis Cache)]
    CoinGecko2 --> Redis
    CoinGecko3 --> Redis
    
    CoinGecko1 --> CoinGeckoAPI[CoinGecko API]
    CoinGecko2 --> CoinGeckoAPI
    CoinGecko3 --> CoinGeckoAPI
    
    QueryAnalysis --> GeminiAI[Google Gemini AI]
    FormatResponse --> GeminiAI
```

### Query Processing Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant LangGraph as LangGraph Workflow
    participant GeminiAI
    participant CoinGecko
    participant Redis
    
    User->>Frontend: Submit query
    Frontend->>LangGraph: Start workflow
    
    rect rgb(240, 248, 255)
        note right of LangGraph: Query Analysis Node
        LangGraph->>GeminiAI: Analyze query
        GeminiAI-->>LangGraph: Extract coin_id, query_type
    end
    
    rect rgb(240, 255, 240)
        note right of LangGraph: Data Fetch Node
        LangGraph->>CoinGecko: Request price data
        CoinGecko->>Redis: Check cache
        
        alt Cache Hit
            Redis-->>CoinGecko: Return cached data
        else Cache Miss
            CoinGecko->>CoinGeckoAPI: Fetch fresh data
            CoinGeckoAPI-->>CoinGecko: Return data
            CoinGecko->>Redis: Cache data
        end
        
        CoinGecko-->>LangGraph: Return price data
    end
    
    rect rgb(255, 240, 240)
        note right of LangGraph: Reflection Node
        alt Data Not Found
            LangGraph->>GeminiAI: Refine coin_id
            GeminiAI-->>LangGraph: Suggest alternative
            LangGraph->>CoinGecko: Retry with new coin_id
        end
    end
    
    rect rgb(255, 240, 255)
        note right of LangGraph: Format Response Node
        LangGraph->>GeminiAI: Format response
        GeminiAI-->>LangGraph: Natural language response
    end
    
    LangGraph-->>Frontend: Final response
    Frontend-->>User: Display result
```

### State Management Flow

```mermaid
flowchart TD
    Start([Start]) --> InitState[Initialize State]
    
    subgraph LangGraph Workflow
        InitState --> QueryNode[Query Analysis Node]
        QueryNode --> |Update State| FetchNode[Data Fetch Node]
        FetchNode --> |Check Data| Decision{Data Found?}
        Decision --> |Yes| FormatNode[Format Response Node]
        Decision --> |No| ReflectNode[Reflection Node]
        ReflectNode --> |Update coin_id| FetchNode
        FormatNode --> |Final State| End([End])
    end
    
    subgraph State Management
        State1[(Initial State)]
        State2[(Query State)]
        State3[(Data State)]
        State4[(Final State)]
    end
    
    QueryNode -.-> State2
    FetchNode -.-> State3
    FormatNode -.-> State4
    
    style State1 fill:#f9f,stroke:#333
    style State2 fill:#bbf,stroke:#333
    style State3 fill:#bfb,stroke:#333
    style State4 fill:#fbb,stroke:#333
```

### Caching Mechanism

```mermaid
flowchart TD
    A[Client Request] --> B{Cache Check}
    B -->|Cache Hit| C[Return Cached Data]
    B -->|Cache Miss| D[Fetch from CoinGecko API]
    D --> E[Store in Redis]
    E --> F[Return Fresh Data]
    
    subgraph Redis Cache
    G[(Price Data)]
    H[(Historical Data)]
    end
    
    C -.-> G
    C -.-> H
    E -.-> G
    E -.-> H
```

### Core Services

1. **Main Backend Service** (`/app`)
   - Natural language query processing using Google's Gemini AI
   - LangGraph-based workflow management
   - Request routing and orchestration
   - Rate limiting and error handling

2. **CoinGecko Service** (`/services/coingecko`)
   - Dedicated cryptocurrency data microservice
   - Real-time price data retrieval
   - Historical price data analysis
   - Redis-based caching layer
   - Horizontal scaling support

3. **Frontend Service** (`/streamlit_app.py`)
   - Interactive Streamlit-based UI
   - Real-time data visualization
   - Dynamic price charts
   - System status monitoring

4. **Redis Service**
   - Distributed caching system
   - Performance optimization
   - Service state management

## 📁 Project Structure

```
.
├── app/                        # Main Backend Service
│   ├── core/                  # Core Configuration
│   │   ├── config.py         # Application configuration
│   │   └── logging.py        # Logging setup
│   ├── graph/                # LangGraph Workflow
│   │   ├── nodes.py         # Workflow nodes
│   │   ├── state.py         # State management
│   │   └── workflow.py      # Graph configuration
│   ├── prompts/             # AI Prompts
│   │   └── templates.py     # Prompt templates
│   └── services/            # Service Clients
│       └── coingecko.py     # CoinGecko client will call to microserive of coingecko
│
├── services/                  # Microservices
│   └── coingecko/           # CoinGecko Service
│       ├── main.py          # Service implementation
│       ├── Dockerfile       # Service container
│       └── requirements.txt # Service dependencies
│
├── docker/                    # Docker Configuration
│   ├── backend.Dockerfile   # Backend service
│   └── frontend.Dockerfile  # Frontend service
│
├── main.py                    # Main service entry
├── streamlit_app.py          # Frontend application
├── docker-compose.yml        # Service orchestration
└── requirements.txt          # Main dependencies
```

## ✨ Features

### Natural Language Processing
- Advanced query understanding using Google's Gemini AI
- Automatic cryptocurrency name resolution
- Context-aware response generation
- Query refinement for failed requests

### Cryptocurrency Data
- Real-time price information
- Historical price analysis
- Market capitalization data
- 24-hour price changes
- Interactive price charts

### System Features
- Microservices architecture
- Horizontal scaling capability
- Redis caching layer
- Rate limiting protection
- CORS support
- Comprehensive error handling
- Detailed logging system

### Frontend Interface
- Modern, responsive design
- Real-time data updates
- Interactive charts
- Query suggestions
- Error feedback
- System status monitoring

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Redis (optional for local development)
- Google Gemini API key

### Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd crypto-price-ai-agent
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)
- `PORT`: Port for the CoinGecko service (default: 8001)

### Docker Deployment

1. Build and start all services:
```bash
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:8501
- Main Backend: http://localhost:8000
- CoinGecko Service: http://localhost:8001

### Service Management

Scale the CoinGecko service:
```bash
docker-compose up -d --scale coingecko=3
```

View service logs:
```bash
docker-compose logs -f [service_name]
```

## 📝 API Documentation

### Main Backend Endpoints

#### Query Endpoint
```bash
POST /query
Content-Type: application/json
{
    "query": "What is the current price of Bitcoin?"
}
```