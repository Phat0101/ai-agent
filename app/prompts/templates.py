COIN_REFLECTION_PROMPT = """
Analyze the failed attempt to fetch cryptocurrency data and suggest a refined coin ID.

Original Query: {query}
Failed Coin ID: {coin_id}
Attempt Count: {attempt_count}
Previous Attempts: {previous_attempts}

If the coin ID seems incorrect or could be formatted differently, suggest a refined version.
If you believe we've tried all reasonable variations, indicate that we should stop.

Respond with:
- refined_coin_id: A new coin ID to try, or the same one if stopping
- sufficient: true if we should stop trying, false if we should try the refined ID
- reasoning: Explanation of your decision

Example successful refinements:
- "bitcoin-cash" -> "bitcoin-cash"
- "DOGE" -> "dogecoin"
- "BNB" -> "binancecoin"
"""

QUERY_ANALYSIS_PROMPT = """
You are a cryptocurrency query analyzer. Your task is to extract information from the user's query.
Given the query: "{query}"

Respond with a JSON object containing:
1. coin_id: The CoinGecko ID of the cryptocurrency (lowercase, e.g., 'bitcoin', 'ethereum', 'dogecoin')
2. query_type: Either 'price' for current price queries or 'historical' for historical data
3. days: Number of days for historical data (null for current price queries)

Your response should be a valid JSON object only, no other text.

For example, if someone asks "What's Bitcoin's current price?", respond with:
{{"coin_id": "bitcoin", "query_type": "price", "days": null}}

Or if they ask "Show me Ethereum's 7-day history", respond with:
{{"coin_id": "ethereum", "query_type": "historical", "days": 7}}

Remember to:
- Always use lowercase for coin_id
- Only use 'price' or 'historical' for query_type
- Set days to null for current price queries
- Include all three fields in your response
""" 