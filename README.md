# Finance Mausi Agent

An intelligent agent built with LangChain and Anthropic models that uses Model Context Protocol (MCP) tools to access:
- Web resources
- Tickr data
- AWS knowledge base

## Features

- 🤖 Intelligent agent powered by Anthropic's language models
- 🛠️ MCP tools integration for accessing various data sources
- 🌐 Web access capabilities
- 📊 Tickr data integration
- ☁️ AWS knowledge base access

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export ANTHROPIC_API_KEY=your_api_key
```

3. Start the MCP servers:
```bash
python servers/web_server.py
python servers/tickr_server.py
python servers/aws_server.py
```

4. Run the agent:
```bash
python agent.py
```

## Project Structure

```
.
├── README.md
├── requirements.txt
├── agent.py           # Main agent implementation
└── servers/
    ├── web_server.py    # Web access MCP server
    ├── tickr_server.py  # Tickr data MCP server
    └── aws_server.py    # AWS knowledge base MCP server
```

## License

MIT License 