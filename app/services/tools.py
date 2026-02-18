import yfinance as yf
import pandas as pd

def get_market_news(ticker: str) -> list:
    """
    Fetches the latest news for a given ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        # Simplify news to just title and publisher for the LLM
        return [{"title": n['title'], "publisher": n['publisher']} for n in news[:5]]
    except Exception as e:
        return [f"Error fetching news: {e}"]

def get_detailed_stats(ticker: str) -> dict:
    """
    Fetches detailed financial statistics for a ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "dividendYield": info.get("dividendYield"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow")
        }
    except Exception as e:
        return {"error": str(e)}

# Tool definitions for OpenAI/Ollama client
AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_market_news",
            "description": "Get latest news for a stock ticker to understand market sentiment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "The stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_detailed_stats",
            "description": "Get detailed financial ratios and stats for a stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "The stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        }
    }
]

# Map names to functions for easy calling
TOOL_MAP = {
    "get_market_news": get_market_news,
    "get_detailed_stats": get_detailed_stats
}
