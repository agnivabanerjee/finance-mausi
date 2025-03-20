# Standard library imports
import json

# Third-party imports
import aiohttp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WebAccess")


@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web for information"""
    async with aiohttp.ClientSession() as session:
        # This is a placeholder. In a real implementation, you would use a proper search API
        search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
        async with session.get(search_url) as response:
            result = await response.text()
            return json.loads(result)


@mcp.tool()
async def fetch_webpage(url: str) -> str:
    """Fetch and return the contents of a webpage"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


if __name__ == "__main__":
    mcp.run(transport="stdio")
