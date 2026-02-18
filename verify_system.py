import time
import json
import os
from app.services.trading_service import TradingService

def verify_system():
    print("🚀 Starting End-to-End Verification...")
    ts = TradingService()
    
    if ts.mode != "ALPACA":
        print("❌ System is NOT in Alpaca mode. Skipping verification.")
        return

    print(f"✅ Trading Mode: {ts.mode}")
    
    # 1. Initial State
    initial_acc = ts.get_account_info()
    initial_agent_cash = initial_acc.agent_portfolio.get("cash", 0)
    print(f"💰 Initial Equity: ${initial_acc.equity:,.2f}")
    print(f"🤖 Initial Agent Cash: ${initial_agent_cash:,.2f}")

    # 2. Manual Trade
    symbol_man = "AMD"
    qty_man = 1
    print(f"\n👤 Placing MANUAL buy for {qty_man} {symbol_man}...")
    res_man = ts.place_order(symbol_man, qty_man, "buy", source="manual")
    print(f"   Result: {res_man}")
    
    if "error" in res_man:
        print("❌ Manual trade failed!")
    else:
        print("✅ Manual trade placed.")

    # 3. Agent Trade
    symbol_agent = "INTC"
    qty_agent = 2
    print(f"\n🤖 Placing AGENT buy for {qty_agent} {symbol_agent}...")
    res_agent = ts.place_order(symbol_agent, qty_agent, "buy", source="agent")
    print(f"   Result: {res_agent}")

    if "error" in res_agent:
        print("❌ Agent trade failed!")
    else:
        print("✅ Agent trade placed.")

    time.sleep(2) # Give a moment for file I/O

    # 4. Verify Trade History
    print("\n📜 Verifying Trade History...")
    history = ts.get_trade_history()
    last_trades = history[-2:]
    
    man_trade = next((t for t in last_trades if t['symbol'] == symbol_man and t['source'] == 'manual'), None)
    agent_trade = next((t for t in last_trades if t['symbol'] == symbol_agent and t['source'] == 'agent'), None)

    if man_trade:
        print(f"✅ Manual trade found in history: {man_trade['qty']} {man_trade['symbol']} @ ${man_trade['price']}")
    else:
        print("❌ Manual trade NOT found in history!")

    if agent_trade:
        print(f"✅ Agent trade found in history: {agent_trade['qty']} {agent_trade['symbol']} @ ${agent_trade['price']}")
    else:
        print("❌ Agent trade NOT found in history!")

    # 5. Verify Agent Portfolio Sync
    print("\n💼 Verifying Agent Portfolio Sync...")
    updated_acc = ts.get_account_info()
    updated_agent_cash = updated_acc.agent_portfolio.get("cash", 0)
    
    expected_deduction = (agent_trade['price'] * qty_agent) if agent_trade else 0
    # Allow for slight float precision differences
    if abs(initial_agent_cash - updated_agent_cash - expected_deduction) < 1.0:
        print(f"✅ Agent cash updated correctly. New Balance: ${updated_agent_cash:,.2f} (Deduced ~${expected_deduction:.2f})")
    else:
        print(f"❌ Agent cash mismatch! Initial: {initial_agent_cash}, Current: {updated_agent_cash}, Expected Deduction: {expected_deduction}")

    # 6. Verify Positions / Orders
    print("\n📊 Verifying Orders/Positions...")
    orders = ts.get_orders()
    positions = ts.get_positions()
    
    man_orders = [o for o in orders if o['symbol'] == symbol_man]
    agent_orders = [o for o in orders if o['symbol'] == symbol_agent]
    
    man_pos = [p for p in positions if p.symbol == symbol_man]
    agent_pos = [p for p in positions if p.symbol == symbol_agent]

    if man_orders or man_pos:
        print(f"✅ Manual trade visible as Order/Position.")
    else:
        print("❌ Manual trade NOT visible in API!")

    if agent_orders or agent_pos:
        print(f"✅ Agent trade visible as Order/Position.")
    else:
        print("❌ Agent trade NOT visible in API!")

    # 7. Performance History
    print("\n📈 Verifying Performance History...")
    if os.path.exists("performance_history.json"):
        with open("performance_history.json", "r") as f:
            perf = json.load(f)
            if perf:
                print(f"✅ Performance history exists with {len(perf)} entries. Last equity: ${perf[-1]['equity']:,.2f}")
            else:
                print("❌ Performance history is empty!")
    else:
        print("❌ Performance history file not found!")

    print("\n🏁 Verification Complete.")

if __name__ == "__main__":
    verify_system()
