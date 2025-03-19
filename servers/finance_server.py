import os
import asyncio
import nest_asyncio
import httpx
import logging
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

# Create a global httpx client
http_client = httpx.AsyncClient()

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

    :argument: symbol (str): The stock symbol to fetch.
    :argument: interval (str): The time interval for the data (default: "5min").
    :argument: datatype (str): The response data type (default: "json").
    :argument: adjusted (bool): The adjusted data flag (default: True).
    :argument: extended_hours (bool): The extended hours flag (default: True).
    :argument: outputsize (str): The output size for the data (default: "compact").
    :argument: month (str): The month of the data (default: None).

    :returns: The intraday stock data.
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
        response = await http_client.get(API_BASE_URL, params=https_params)
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

    :argument: symbol (str): The stock symbol to fetch.
    :argument: datatype (str): The response data type (default: "json").

    :returns: The daily stock data.
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
        response = await http_client.get(API_BASE_URL, params=https_params)
        logger.debug(f"API response status: {response.status_code}")
        response.raise_for_status()
        result = response.text if datatype == "csv" else response.json()
        logger.debug(f"API request successful, returning data type: {type(result)}")
        return result
    except Exception as e:
        logger.error(f"Error in fetch_time_series_daily: {str(e)}")
        raise


async def cleanup():
    await http_client.aclose()


if __name__ == "__main__":
    logger.info("Starting Finance Server...")
    try:
        mcp.run(transport="stdio")
    finally:
        asyncio.run(cleanup())
