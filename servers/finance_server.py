import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


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

    :argument: symbol (str): The stock symbol to fetch.
    :argument: interval (str): The time interval for the data (default: "5min").
    :argument: datatype (str): The response data type (default: "json").
    :argument: adjusted (bool): The adjusted data flag (default: True).
    :argument: extended_hours (bool): The extended hours flag (default: True).
    :argument: outputsize (str): The output size for the data (default: "compact").
    :argument: month (str): The month of the data (default: None).

    :returns: The intraday stock data.
    """

    https_params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "datatype": datatype,
        "adjusted": adjusted,
        "outputsize": outputsize,
        "extended_hours": extended_hours,
        "month": month,
        "apikey": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(API_BASE_URL, params=https_params)
        response.raise_for_status()
        return response.text if datatype == "csv" else response.json()


async def fetch_time_series_daily(
    symbol: str, datatype: str = "json", outputsize: str = "compact"
) -> dict[str, str] | str:
    """
    Fetch daily stock data from the Alpha Vantage API.

    :argument: symbol (str): The stock symbol to fetch.
    :argument: datatype (str): The response data type (default: "json").

    :returns: The daily stock data.
    """

    https_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "datatype": datatype,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(API_BASE_URL, params=https_params)
        response.raise_for_status()
        return response.text if datatype == "csv" else response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
