"""
Finance Server Module

This module implements an MCP server that provides financial data tools using the AlphaVantage API.
It offers tools for fetching intraday and daily stock price data.

The module uses FastMCP to expose the following tools:
- fetch_intraday: Get intraday stock price data
- fetch_time_series_daily: Get daily stock price data

Environment Variables:
    ALPHAVANTAGE_API_KEY: API key for accessing AlphaVantage services

Author: Your Name
License: MIT
"""

# Standard library imports
import logging
import os

# Third-party imports
import httpx
import nest_asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Apply nest_asyncio at the module level
nest_asyncio.apply()

load_dotenv()

mcp = FastMCP("FinanceData")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
API_BASE_URL = "https://www.alphavantage.co/query"


@mcp.tool()
async def fetch_intraday(
    symbol: str,
    interval: str = "60min",
    datatype: str = "json",
    adjusted: bool = True,
    extended_hours: bool = True,
    outputsize: str = "compact",
    month: str = None,
) -> dict[str, str] | str:
    """
    Fetch intraday stock data from the Alpha Vantage API.

    This function retrieves intraday stock price data with configurable parameters
    for time interval, data format, and other options.

    Args:
        symbol (str): The stock symbol to fetch (e.g., 'AAPL', 'GOOGL')
        interval (str, optional): Time interval between data points. Defaults to "60min".
            Valid values: '1min', '5min', '15min', '30min', '60min'
        datatype (str, optional): Response format. Defaults to "json".
            Valid values: 'json', 'csv'
        adjusted (bool, optional): Whether to return adjusted data. Defaults to True.
        extended_hours (bool, optional): Include extended hours data. Defaults to True.
        outputsize (str, optional): Amount of data to return. Defaults to "compact".
            Valid values: 'compact', 'full'
        month (str, optional): Specific month to fetch (YYYY-MM format). Defaults to None.

    Returns:
        Union[dict[str, str], str]: Stock data in either JSON or CSV format

    Raises:
        Exception: If the API request fails or returns an error
    """
    logger.debug(f"fetch_intraday called with symbol={symbol}, interval={interval}")

    https_params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "datatype": datatype,
        "adjusted": "true" if adjusted else "false",
        "outputsize": outputsize,
        "extended_hours": "true" if extended_hours else "false",
        "month": month,
        "apikey": API_KEY,
    }

    try:
        logger.debug(f"Making API request with params: {https_params}")
        # Create a new client for each request
        async with httpx.AsyncClient() as client:
            response = await client.get(API_BASE_URL, params=https_params, timeout=30.0)
            logger.debug(f"API response status: {response.status_code}")
            response.raise_for_status()
            result = response.text if datatype == "csv" else response.json()
            logger.debug(f"API request successful, returning data type: {type(result)}")
            return result
    except Exception as e:
        logger.error(f"Error in fetch_intraday: {str(e)}")
        raise


@mcp.tool()
async def fetch_time_series_daily(
    symbol: str, datatype: str = "json", outputsize: str = "compact"
) -> dict[str, str] | str:
    """
    Fetch daily stock data from the Alpha Vantage API.

    This function retrieves daily stock price data with options for
    data format and amount of historical data.

    Args:
        symbol (str): The stock symbol to fetch (e.g., 'AAPL', 'GOOGL')
        datatype (str, optional): Response format. Defaults to "json".
            Valid values: 'json', 'csv'
        outputsize (str, optional): Amount of data to return. Defaults to "compact".
            Valid values: 'compact' (latest 100 data points), 'full' (all data points)

    Returns:
        Union[dict[str, str], str]: Stock data in either JSON or CSV format

    Raises:
        Exception: If the API request fails or returns an error
    """
    logger.debug(f"fetch_time_series_daily called with symbol={symbol}")

    https_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "datatype": datatype,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }

    try:
        logger.debug(f"Making API request with params: {https_params}")
        # Create a new client for each request
        async with httpx.AsyncClient() as client:
            response = await client.get(API_BASE_URL, params=https_params, timeout=30.0)
            logger.debug(f"API response status: {response.status_code}")
            response.raise_for_status()
            result = response.text if datatype == "csv" else response.json()
            logger.debug(f"API request successful, returning data type: {type(result)}")
            return result
    except Exception as e:
        logger.error(f"Error in fetch_time_series_daily: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info("Starting Finance Server...")
    mcp.run(transport="stdio")
