# Technical Documentation

This document provides detailed technical information about the internal workings of the Crypto Price AI Agent.

## Query Processing Flow

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

## State Management Flow

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

## Caching Mechanism

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

## Technical Details

### LangGraph Workflow
The application uses LangGraph to orchestrate the natural language processing workflow:
1. **Query Analysis**: Extracts cryptocurrency information and query type
2. **Data Fetching**: Retrieves price data with caching
3. **Reflection**: Handles failed queries with alternative suggestions
4. **Response Formatting**: Generates natural language responses

### State Management
The workflow maintains state throughout the process:
- Initial State: Raw user query
- Query State: Analyzed query with extracted parameters
- Data State: Retrieved cryptocurrency data
- Final State: Formatted response

### Caching Strategy
Redis is used for caching with the following features:
- Separate cache keys for price and historical data
- 60-second TTL for all cached data
- Automatic cache invalidation
- Cache hit/miss logging 