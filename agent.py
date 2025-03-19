import gradio as gr
import logging
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
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

@asynccontextmanager
async def create_mcp_agent():
    """Create an MCP agent with all available tools."""
    logger.info("Creating MCP agent...")
    async with MultiServerMCPClient() as mcp_client:
        # Connect to finance server
        logger.debug("Connecting to finance server...")
        await mcp_client.connect_to_server_via_stdio(
            "finance",
            command="python",
            args=["servers/finance_server.py"]
        )
        
        # Get all tools
        mcp_tools = mcp_client.get_tools()
        logger.debug(f"Loaded tools: {mcp_tools}")
        
        # Create the agent
        agent = create_react_agent(model, mcp_tools)
        logger.info("Agent created successfully")
        
        try:
            yield agent
        finally:
            logger.info("Cleaning up MCP agent...")


class FinanceAgent:
    def __init__(self):
        self.agent = None
        self.memory = ConversationBufferMemory()
        self.conversation = None
        self.mcp_client = None
        logger.info("FinanceAgent initialized")

    async def initialize_agent(self):
        """Initialize the MCP client and agent if not already initialized."""
        if self.agent is None:
            logger.info("Initializing MCP client and agent...")
            self.mcp_client = MultiServerMCPClient()
            await self.mcp_client.__aenter__()
            
            try:
                # Connect to finance server
                logger.debug("Connecting to finance server...")
                await self.mcp_client.connect_to_server_via_stdio(
                    "finance",
                    command="python",
                    args=["servers/finance_server.py"]
                )
                
                # Get all tools
                mcp_tools = self.mcp_client.get_tools()
                logger.debug(f"Loaded tools: {mcp_tools}")
                
                # Create the agent
                self.agent = create_react_agent(model, mcp_tools)
                self.conversation = ConversationChain(
                    llm=model, memory=self.memory, verbose=True
                )
                logger.info("Agent created successfully")
            except Exception as e:
                # Clean up if initialization fails
                if self.mcp_client:
                    await self.mcp_client.__aexit__(None, None, None)
                    self.mcp_client = None
                raise e

    async def cleanup(self):
        """Cleanup MCP client resources."""
        if self.mcp_client:
            logger.info("Cleaning up MCP client...")
            await self.mcp_client.__aexit__(None, None, None)
            self.mcp_client = None
            self.agent = None

    async def process_message(self, message: str, history: List[List[str]]) -> str:
        try:
            if self.agent is None:
                logger.info("First message received, initializing agent...")
                await self.initialize_agent()
            
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
            # Try to cleanup on error
            await self.cleanup()
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
