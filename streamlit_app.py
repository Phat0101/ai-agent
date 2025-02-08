import streamlit as st
import requests
import json
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Crypto Price AI Agent",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better text formatting
st.markdown("""
    <style>
    .crypto-response {
        background-color: grey;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 18px;
        line-height: 1.5;
        color: white
    }
    </style>
""", unsafe_allow_html=True)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")

def format_response_text(text: str) -> str:
    """Clean and format the response text"""
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    # Ensure proper spacing after punctuation
    text = re.sub(r'([.,!?])(\S)', r'\1 \2', text)
    # Fix spacing around currency symbols
    text = re.sub(r'(\$)(\s+)', r'\1', text)
    return text

def query_agent(query: str) -> dict:
    """Send query to FastAPI backend"""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {str(e)}")
        return None

def plot_historical_data(data: dict) -> go.Figure:
    """Create a plotly figure for historical price data"""
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["price"],
            mode="lines",
            name="Price",
            line=dict(color="#1f77b4", width=2)
        )
    )
    
    fig.update_layout(
        title="Historical Price Data",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig

# Sidebar
with st.sidebar:
    st.title("💰 Crypto Price AI")
    st.markdown("""
    Ask me about cryptocurrency prices! Examples:
    - What's the current price of Bitcoin?
    - Show me Ethereum's price history for the last 7 days
    - What's DOGE worth right now?
    """)
    
    # API Status
    try:
        health_response = requests.get(f"{API_URL}/health")
        if health_response.status_code == 200:
            st.success("API Status: Online")
        else:
            st.error("API Status: Offline")
    except:
        st.error("API Status: Offline")

# Main content
st.title("Cryptocurrency Price Assistant")

# Query input
query = st.text_input(
    "Enter your query",
    placeholder="e.g., What's the current price of Bitcoin?"
)

if query:
    with st.spinner("Processing your query..."):
        result = query_agent(query)
        
        if result:
            # Display the AI response
            st.markdown("### Response")
            formatted_response = format_response_text(result["result"])
            st.markdown(f'<div class="crypto-response">{formatted_response}</div>', unsafe_allow_html=True)
            
            # Display data visualization if it's historical data
            if "prices" in result["data"]:
                st.markdown("### Price Chart")
                fig = plot_historical_data(result["data"])
                st.plotly_chart(fig, use_container_width=True)
            
            # Display raw data in expander
            with st.expander("View Raw Data"):
                st.json(result["data"])

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with Streamlit, FastAPI, and LangGraph</p>
    </div>
    """,
    unsafe_allow_html=True
) 