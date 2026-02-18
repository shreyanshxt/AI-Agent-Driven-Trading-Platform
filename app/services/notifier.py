import os
import logging
from datetime import datetime

class Notifier:
    def __init__(self, log_file: str = "agent_activity.log"):
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("FinSightNotifier")

    def notify(self, message: str, level: str = "info"):
        """
        Logs a message and prints to console. 
        Placeholder for Slack/Discord integration.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "trade":
            self.logger.warning(f"ACTION REQUIRED / TRADE EXECUTED: {message}")
            
        print(f"NOTIFIER: {full_message}")

    def notify_trade(self, ticker: str, side: str, qty: int, reasoning: str):
        msg = f"Trade Executed: {side.upper()} {qty} shares of {ticker}. Reasoning: {reasoning}"
        self.notify(msg, level="trade")

    def notify_analysis(self, ticker: str, signal: str, reasoning: str):
        msg = f"Analysis for {ticker}: {signal}. Reasoning: {reasoning}"
        self.notify(msg)
