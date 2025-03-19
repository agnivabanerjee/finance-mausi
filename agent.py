import os
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatOpenAI(model="gpt-4")

async def run_agent():
    # Create server parameters for each MCP server
    web_server_params = StdioServerParameters(
        command="python",
        args=["servers/web_server.py"],
    )
    
    tickr_server_params = StdioServerParameters(
        command="python",
        args=["servers/tickr_server.py"],
    )
    
    aws_server_params = StdioServerParameters(
        command="python",
        args=["servers/aws_server.py"],
    )
    
    # Create a list to store all tools
    all_tools = []
    
    # Connect to web server
    async with stdio_client(web_server_params) as (web_read, web_write):
        async with ClientSession(web_read, web_write) as web_session:
            await web_session.initialize()
            web_tools = await load_mcp_tools(web_session)
            all_tools.extend(web_tools)
    
        # Connect to tickr server
        async with stdio_client(tickr_server_params) as (tickr_read, tickr_write):
            async with ClientSession(tickr_read, tickr_write) as tickr_session:
                await tickr_session.initialize()
                tickr_tools = await load_mcp_tools(tickr_session)
                all_tools.extend(tickr_tools)
    
            # Connect to AWS server
            async with stdio_client(aws_server_params) as (aws_read, aws_write):
                async with ClientSession(aws_read, aws_write) as aws_session:
                    await aws_session.initialize()
                    aws_tools = await load_mcp_tools(aws_session)
                    all_tools.extend(aws_tools)
    
                # Create and run the agent
                agent = create_react_agent(model, all_tools)
                
                # Example query
                response = await agent.ainvoke({"messages": "What resources are available?"})
                print(response)

if __name__ == "__main__":
    asyncio.run(run_agent()) 