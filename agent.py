import os
import asyncio
import gradio as gr
from typing import List, Dict, Any
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0,
    max_tokens=8192,
    timeout=None,
    max_retries=2,
)


class FinanceAgent:
    def __init__(self):
        self.agent = None
        self.memory = ConversationBufferMemory()
        self.conversation = None
        self.all_tools = []

    async def initialize_servers(self):
        # Create server parameters for each MCP server
        web_server_params = StdioServerParameters(
            command="python",
            args=["servers/web_server.py"],
        )

        finance_server_params = StdioServerParameters(
            command="python",
            args=["servers/finance_server.py"],
        )

        aws_server_params = StdioServerParameters(
            command="python",
            args=["servers/aws_server.py"],
        )

        # Connect to web server
        # async with stdio_client(web_server_params) as (web_read, web_write):
        #     async with ClientSession(web_read, web_write) as web_session:
        #         await web_session.initialize()
        #         web_tools = await load_mcp_tools(web_session)
        #         self.all_tools.extend(web_tools)

        # Connect to finance server
        async with stdio_client(finance_server_params) as (
            finance_read,
            finance_write,
        ):
            async with ClientSession(
                finance_read, finance_write
            ) as finance_session:
                await finance_session.initialize()
                finance_tools = await load_mcp_tools(finance_session)
                self.all_tools.extend(finance_tools)

        # # Connect to AWS server
        # async with stdio_client(aws_server_params) as (aws_read, aws_write):
        #     async with ClientSession(aws_read, aws_write) as aws_session:
        #         await aws_session.initialize()
        #         aws_tools = await load_mcp_tools(aws_session)
        #         self.all_tools.extend(aws_tools)

        # Create the agent with tools and memory
        self.agent = create_react_agent(model, self.all_tools)
        self.conversation = ConversationChain(
            llm=model, memory=self.memory, verbose=True
        )

    async def process_message(self, message: str, history: List[List[str]]) -> str:
        if self.agent is None:
            await self.initialize_servers()

        try:
            # Get response from agent
            response = await self.agent.ainvoke({"messages": message})

            # Update conversation memory
            self.memory.save_context({"input": message}, {"output": response})

            return response
        except Exception as e:
            return f"Error processing your request: {str(e)}"


def create_gradio_interface():
    # Initialize the agent
    finance_agent = FinanceAgent()

    # Create the Gradio interface
    chatbot = gr.ChatInterface(
        finance_agent.process_message,
        title="Finance Mausi - Your AI Financial Assistant",
        description="Ask me anything about stocks, AWS services, or general financial information!",
        theme="soft",
        examples=[
            "What's the current price of AAPL stock?",
            "Tell me about AWS EC2 service limits",
            "How has Tesla stock performed over the last week?",
            "What are the basic AWS services for hosting a web application?",
        ],
        additional_inputs=None,
        additional_outputs=None,
    )

    return chatbot


if __name__ == "__main__":
    # Create and launch the Gradio interface
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
