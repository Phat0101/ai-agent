# AI Agent Interview Task: Cryptocurrency Price Query using CoinGecko & langgraph

## Task Overview

You are required to build an AI Agent that can respond to user queries about cryptocurrency prices using the **CoinGecko API** and **langgraph** for data processing. The agent should:

*   Accept user queries in natural language (e.g., "What is the price of Bitcoin?").
*   Fetch real-time cryptocurrency prices from the **CoinGecko API**.
*   Process and store relevant data using **langgraph**.
*   Return a structured response with the requested information.

## Requirements

**1. AI Agent Functionality**

*   The agent should process text input to extract the relevant cryptocurrency name.
*   Fetch the latest price from the CoinGecko API.
*   Return a response like:
*   The current price of Bitcoin (BTC) is $142,500.00.

**2. CoinGecko API Integration**

*   Use the **CoinGecko API** to fetch cryptocurrency prices.
*   Ensure proper handling of API errors and rate limits.

**3. langgraph for AI Framework (tooling)**

*   Use **langgraph** to structure and log data (e.g., store fetched prices).
*   Create a lightweight storage solution (e.g., saving data to a local or cloud-based CSV or database).

**4. Deployment & Execution**

*   Package the AI Agent into a Python script or FastAPI endpoint.
*   Provide a way to test it (e.g., CLI input, Flask/FastAPI app, or a simple chatbot interface).

## Bonus Points

Candidates will receive extra points for:

*   ✅ Caching responses to reduce API calls (e.g., using Redis, Postgres).
*   ✅ Supporting multiple query types like:
    *   "What is the market cap of Ethereum?"
    *   "What was the price of Dogecoin 7 days ago?"
*   ✅ Implementing error handling & logging.
*   ✅ Writing clean, modular, and well-documented code.

## Submission Instructions

*   Upload your code to a **GitHub repo** or share it as a **zip file**.
*   Provide a **README** with setup instructions and example queries.
*   If deploying as an API, share a **live endpoint** (optional).

## Evaluation Criteria

*   **Correctness** – Does the agent correctly fetch & return prices?
*   **Code Quality** – Is the code modular, readable, and documented?
*   **Efficiency** - Does it handle API limits & caching effectively?
*   **Scalability** - Can it be extended to support more queries?