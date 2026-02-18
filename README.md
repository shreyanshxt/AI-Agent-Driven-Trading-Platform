# FinSight: AI-Agent Driven Trading Platform 📈🤖

FinSight is a state-of-the-art, autonomous trading platform powered by Local LLMs and real-time market data. It combines advanced financial analysis with autonomous trade execution, providing a seamless bridge between complex market signals and actionable trades.

## ✨ Features

### 🧠 AI-Driven Analysis
- **Autonomous Decision Making**: Uses Local LLMs (via Ollama) to analyze technical indicators and news sentiment.
* **Signal Generation**: Produces clear `BUY`, `SELL`, or `HOLD` signals with deep reasoning.
- **Dynamic Context**: Integrates real-time price history and technical indicators (RSI, MACD, Bollinger Bands).

### 📊 Interactive Dashboard
- **Glassmorphic UI**: A premium, modern interface with dark mode and vibrant accents.
- **3D Global Visualization**: Visualize global headquarters and market activity on a rotating 3D globe.
- **Real-time Portfolio Tracking**: Monitor equity curves, buying power, and detailed position management.
- **Live Activity Feed**: Real-time notifications of agent analysis and executed trades.

### ⚡ Technical Excellence
- **Hybrid Execution**: Supports both Alpaca (Paper Trading) and a robust Local Simulation mode.
- **Parallel Backtesting**: Analyze historical data while maintaining live monitoring.
- **Microservice Architecture**: Built with FastAPI for high performance and scalability.
- **Reliable Persistence**: JSON-based state management with file locking for data integrity.

## 🚀 Quick Start

### Prerequisites
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
2. [Ollama](https://ollama.com/) installed and running locally (`ollama serve`).
3. (Optional) AlphaVantage API Key (for indicator data).
4. (Optional) Alpaca API Keys (for paper trading).

### Installation & Deployment

1. **Clone and Configure**
   ```bash
   git clone https://github.com/shreyanshxt/AI-Agent-Driven-Trading-Platform.git
   cd AI-Agent-Driven-Trading-Platform
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Launch with Docker**
   ```bash
   docker-compose up --build
   ```

3. **Interact**
   - **Dashboard**: [http://localhost:8000](http://localhost:8000)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠 Project Structure
- `app/main.py`: Core FastAPI application and endpoints.
- `app/services/agent_brain.py`: The "brain" of the autonomous agent.
- `app/services/trading_service.py`: Multi-mode trading execution layer.
- `app/services/llm_engine.py`: LLM integration and prompt engineering.
- `app/services/data_fetcher.py`: Real-time market data and indicator fetching.

---
*Built with ❤️ by [Shreyansh Singh](https://github.com/shreyanshxt)*
