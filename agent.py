import os
import asyncio
import gradio as gr
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize the model
logger.info("Initializing ChatAnthropic model...")
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
        logger.info("FinanceAgent initialized")

    async def initialize_servers(self):
        logger.info("Initializing MCP servers...")
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

        try:
            # Connect to finance server
            logger.debug("Connecting to finance server...")
            async with stdio_client(finance_server_params) as (
                finance_read,
                finance_write,
            ):
                async with ClientSession(finance_read, finance_write) as finance_session:
                    await finance_session.initialize()
                    finance_tools = await load_mcp_tools(finance_session)
                    logger.debug(f"Loaded finance tools: {[tool.name for tool in finance_tools]}")
                    self.all_tools.extend(finance_tools)
        except Exception as e:
            logger.error(f"Error initializing servers: {str(e)}")
            raise
        # Create the agent with tools and memory
        logger.info(f"Creating agent with {len(self.all_tools)} tools")
        self.agent = create_react_agent(model, self.all_tools)
        self.conversation = ConversationChain(
            llm=model, memory=self.memory, verbose=True
        )
        logger.info("Agent creation complete")

    async def process_message(self, message: str, history: List[List[str]]) -> str:
        if self.agent is None:
            logger.info("First message received, initializing servers...")
            await self.initialize_servers()

        try:
            logger.debug(f"Processing message: {message}")
            # Get response from agent
            logger.debug("Invoking agent...")
            response = await self.agent.ainvoke({"messages": message})
            logger.debug(f"Agent response: {response}")

            ai_message = response["messages"][-1].content
            logger.debug(f"Extracted AI message: {ai_message}")

            # Update conversation memory
            self.memory.save_context({"input": str(message)}, {"output": ai_message})
            logger.debug("Conversation memory updated")

            return ai_message
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return f"Error processing your request: {str(e)}"


def create_gradio_interface():
    logger.info("Creating Gradio interface...")
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
    logger.info("Gradio interface created")
    return chatbot


if __name__ == "__main__":
    # Create and launch the Gradio interface
    logger.info("Starting Finance Mausi application...")
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
