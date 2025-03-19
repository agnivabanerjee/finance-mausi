# Finance Mausi Agent

An intelligent agent built with LangChain and Anthropic models that uses Model Context Protocol (MCP) tools to access:
- Web resources
- Financial market data
- AWS knowledge base

## Features

- 🤖 Intelligent agent powered by Anthropic's Claude 3 Sonnet
- 🛠️ MCP tools integration for accessing various data sources
- 🌐 Web access capabilities
- 📊 Real-time financial data using yfinance
- ☁️ AWS knowledge base access with Kendra integration
- 💬 User-friendly Gradio chat interface

## Setup

### Environment Variables

Create a `.env` file with the following variables:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=your_aws_region
AWS_KENDRA_INDEX_ID=your_kendra_index_id
```

### Running with Docker (Recommended)

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Access the chat interface at: http://localhost:7860

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the MCP servers (in separate terminals):
```bash
python servers/web_server.py
python servers/finance_server.py
python servers/aws_server.py
```

3. Run the agent:
```bash
python agent.py
```

## Project Structure

```
.
├── README.md
├── requirements.txt
├── agent.py           # Main agent implementation
├── Dockerfile
├── docker-compose.yml
└── servers/
    ├── web_server.py    # Web access MCP server
    ├── finance_server.py # Financial data MCP server
    └── aws_server.py    # AWS knowledge base MCP server
```

## Available Commands

The agent can help you with:
- Getting real-time stock prices and market data
- Searching AWS documentation and service information
- Retrieving company information and financial news
- Checking AWS service health and limits

Example queries:
- "What's the current price of AAPL stock?"
- "Tell me about AWS EC2 service limits"
- "How has Tesla stock performed over the last week?"
- "What are the basic AWS services for hosting a web application?"

## License

MIT License 