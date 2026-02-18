import os
import sys

# Add the project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.services.data_fetcher import MarketDataService
from app.services.llm_engine import FinancialAnalyst
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    print("--- FinSight Agent: Direct Service Test ---")
    
    ticker = "AAPL"
    print(f"1. Initializing services for {ticker}...")
    
    market_service = MarketDataService()
    analyst = FinancialAnalyst()
    
    print("2. Fetching market data...")
    market_data = market_service.get_market_data(ticker)
    
    if not market_data.get("price_data"):
        print("Error: Could not fetch price data.")
        return
        
    price = market_data["price_data"]["current_price"]
    change = market_data["price_data"]["change_percent"]
    print(f"   Success! Price: ${price} ({change}%)")
    
    print("3. Performing AI Analysis (via Ollama)...")
    analysis = analyst.analyze(ticker, market_data)
    
    print("\n--- Final Analysis Result ---")
    print(f"Ticker: {ticker}")
    print(f"Signal: {analysis.get('signal')}")
    print(f"Reasoning: {analysis.get('reasoning')}")

if __name__ == "__main__":
    main()
