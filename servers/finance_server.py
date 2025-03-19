from mcp.server.fastmcp import FastMCP
import yfinance as yf
from typing import List, Dict, Any
from datetime import datetime, timedelta

mcp = FastMCP("FinanceData")

@mcp.tool()
async def get_stock_price(symbol: str) -> Dict[str, Any]:
    """Get the current stock price and basic info for a given symbol"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "price": info.get("regularMarketPrice", 0.0),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange", ""),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_historical_data(symbol: str, days: int = 7) -> List[Dict[str, Any]]:
    """Get historical stock data for a given symbol and number of days"""
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        df = ticker.history(start=start_date, end=end_date)
        
        return [{
            "date": index.strftime("%Y-%m-%d"),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"]
        } for index, row in df.iterrows()]
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
async def get_company_info(symbol: str) -> Dict[str, Any]:
    """Get detailed company information for a given stock symbol"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "description": info.get("longBusinessSummary", ""),
            "website": info.get("website", ""),
            "country": info.get("country", "")
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_market_news(symbol: str = "") -> List[Dict[str, Any]]:
    """Get latest market news, optionally filtered by symbol"""
    try:
        if symbol:
            ticker = yf.Ticker(symbol)
            news = ticker.news
        else:
            # Get news for major indices as a fallback
            indices = ["^GSPC", "^DJI", "^IXIC"]  # S&P 500, Dow Jones, NASDAQ
            news = []
            for idx in indices:
                ticker = yf.Ticker(idx)
                news.extend(ticker.news[:3])  # Get top 3 news from each index
                
        return [{
            "title": item.get("title", ""),
            "publisher": item.get("publisher", ""),
            "link": item.get("link", ""),
            "published": datetime.fromtimestamp(item.get("providerPublishTime", 0)).isoformat()
        } for item in news[:10]]  # Return top 10 news items
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    mcp.run(transport="stdio") 