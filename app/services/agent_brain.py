import asyncio
import json
from app.services.data_fetcher import MarketDataService
from app.services.llm_engine import FinancialAnalyst
from app.services.trading_service import TradingService
from app.services.notifier import Notifier

class AutonomousAgent:
    def __init__(self, model: str = None):
        # Load config
        self.config = self._load_config()
        self.model = model or self.config.get("model", "llama3.1")
        
        self.market_service = MarketDataService()
        self.analyst = FinancialAnalyst(model=self.model)
        self.trading_service = TradingService()
        self.notifier = Notifier()
        self.watchlist = ["AAPL", "NVDA", "BTC-USD", "TSLA"]
        self.interval = 30 # 5 minutes

    def _load_config(self):
        try:
            with open("agent_config.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Config read error: {e}. Using defaults.")
            return {}

    async def run_once(self, ticker: str):
        print(f"--- Autonomous Cycle for {ticker} ---")
        
        # 1. Fetch Data
        data = self.market_service.get_market_data(ticker)
        if not data.get("price_data"):
            print(f"Failed to fetch data for {ticker}")
            return

        # 1.5 Fetch News (Proactive fallback for models without tool-calling)
        from app.services.tools import get_market_news
        print(f"Fetching latest news for {ticker}...")
        data["news"] = get_market_news(ticker)

        # 2. Analyze
        print(f"Analyzing {ticker}...")
        analysis = self.analyst.analyze(ticker, data)
        signal = analysis.get("signal", "HOLD")
        reasoning = analysis.get("reasoning", "")
        
        self.notifier.notify_analysis(ticker, signal, reasoning)

        # 3. Execute Trade (if signal Buy/Sell and logic permits)
        if signal in ["BUY", "SELL"]:
            if not self.config.get("autonomous_enabled", True):
                print(f"Skipping autonomous trade for {ticker}: Disabled in config.")
                return analysis

            side = signal.lower()
            print(f"Autonomous decision: {signal} {ticker}")
            # Calculate quantity based on Agent's available capital
            try:
                account = self.trading_service.get_account_info()
                # Check if it's a dict or object (TradingService returns namespace wrapper usually)
                if isinstance(account, dict):
                    ag_port = account.get("agent_portfolio", {})
                else:
                    ag_port = getattr(account, "agent_portfolio", {})
                
                agent_cash = ag_port.get("cash", 0)
                current_price = data.get("price_data", {}).get("current_price", 0)
                
                if current_price > 0:
                    if side == "buy":
                        # Use up to 20% of available cash per trade for better utilization, or at least 1 share
                        allocation_per_trade = agent_cash * 0.20
                        qty = int(allocation_per_trade / current_price)
                        
                        if qty < 1 and agent_cash >= current_price:
                            qty = 1
                        
                        if qty < 1:
                            print(f"Insufficient agent funds for {ticker}. Cash: ${agent_cash:.2f}, Price: ${current_price:.2f}")
                            return analysis
                    else: # sell
                        # Get held quantity for this ticker
                        ag_pos = ag_port.get("positions", {}).get(ticker, {})
                        qty = ag_pos.get("qty", 0)
                        
                        if qty <= 0:
                            print(f"Skipping SELL for {ticker}: Agent has no shares to sell.")
                            return analysis
                else:
                    print(f"Invalid price for {ticker}: {current_price}")
                    return analysis

            except Exception as e:
                print(f"Error calculating quantity for {ticker}: {e}. Defaulting to 1.")
                qty = 1 
            
            print(f"Agent Attempting to {side.upper()} {qty} shares of {ticker}...")
            result = self.trading_service.place_order(ticker, qty, side, source="agent")
            
            if "error" in result:
                print(f"Trade failed/rejected for {ticker}: {result['error']}")
            else:
                mode_str = " (SIMULATED)" if result.get("mode") == "simulation" else ""
                self.notifier.notify_trade(ticker, side, qty, f"{reasoning}{mode_str}")
                print(f"Trade Successful for {ticker}: {result}")
        
        return analysis

    async def start_monitoring(self):
        print(f"Starting background monitor for: {self.watchlist}")
        while True:
            for ticker in self.watchlist:
                try:
                    # Reload config on every ticker cycle to pick up changes
                    self.config = self._load_config()
                    # Sync analyst model with current config
                    new_model = self.config.get("model", self.model)
                    if new_model != self.analyst.model:
                        print(f"Switching analyst model to: {new_model}")
                        self.analyst.model = new_model
                    
                    await self.run_once(ticker)
                except Exception as e:
                    print(f"Error in monitor cycle for {ticker}: {e}")
            
            print(f"Cycle complete. Waiting {self.interval}s...")
            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    # For standalone testing
    agent = AutonomousAgent()
    asyncio.run(agent.start_monitoring())
