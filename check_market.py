import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

try:
    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    clock = api.get_clock()
    print(f"Timestamp: {clock.timestamp}")
    print(f"Is Open: {clock.is_open}")
    print(f"Next Open: {clock.next_open}")
    print(f"Next Close: {clock.next_close}")
    
    calendar = api.get_calendar(start="2026-02-16", end="2026-02-16")
    if not calendar:
        print("No calendar entry for today (Likely Holiday)")
    else:
        print(f"Calendar: {calendar}")

except Exception as e:
    print(f"Error: {e}")
