from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("TickrData")

@mcp.tool()
async def get_stock_price(symbol: str) -> float:
    """Get the current stock price for a given symbol"""
    # This is a placeholder. In a real implementation, you would connect to a stock API
    return 100.0  # Placeholder value

@mcp.tool()
async def get_historical_data(symbol: str, days: int) -> List[Dict[str, Any]]:
    """Get historical stock data for a given symbol and number of days"""
    # This is a placeholder. In a real implementation, you would fetch real historical data
    return [
        {"date": "2024-03-01", "price": 100.0, "volume": 1000000},
        {"date": "2024-03-02", "price": 101.0, "volume": 1100000},
    ]

@mcp.tool()
async def get_company_info(symbol: str) -> Dict[str, Any]:
    """Get company information for a given stock symbol"""
    # This is a placeholder. In a real implementation, you would fetch real company data
    return {
        "name": "Example Corp",
        "sector": "Technology",
        "market_cap": 1000000000,
        "pe_ratio": 20.5
    }

if __name__ == "__main__":
    mcp.run(transport="stdio") 