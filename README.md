# Finance Mausi

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

## Prerequisites

- Docker and Docker Compose
- Google Cloud Platform account with Vertex AI API enabled
- AWS account (optional, for AWS features)
- Python 3.11+

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance-mausi.git
cd finance-mausi
```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required values:
     ```
     # Required
     GOOGLE_CLOUD_PROJECT=your-project-id
     GOOGLE_CLOUD_LOCATION=us-central1 (or your preferred region)
     
     # Optional (for AWS features)
     AWS_ACCESS_KEY_ID=your-aws-access-key
     AWS_SECRET_ACCESS_KEY=your-aws-secret-key
     AWS_DEFAULT_REGION=us-east-1
     ```

3. Set up Google Cloud credentials:
   - Create a service account in Google Cloud Console
   - Download the service account key
   - Save it as `credentials/google-credentials.json`
   - Ensure the service account has access to Vertex AI API

4. Build and run with Docker:
```bash
docker compose up --build
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| GOOGLE_CLOUD_PROJECT | Your Google Cloud Project ID | Yes | - |
| GOOGLE_CLOUD_LOCATION | Google Cloud region | Yes | us-central1 |
| GOOGLE_APPLICATION_CREDENTIALS | Path to service account key | Yes | ./credentials/google-credentials.json |
| AWS_ACCESS_KEY_ID | AWS Access Key | No | - |
| AWS_SECRET_ACCESS_KEY | AWS Secret Key | No | - |
| AWS_DEFAULT_REGION | AWS Region | No | us-east-1 |
| DEBUG | Enable debug mode | No | false |
| LOG_LEVEL | Logging level | No | INFO |

## Architecture

The application is built using:
- LangChain for agent orchestration
- Google Vertex AI (Claude 3 Sonnet) for natural language processing
- Gradio for the web interface
- Docker for containerization

## Development

To run the application in development mode:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python agent.py
```

## Security Notes

- Never commit the `.env` file or `google-credentials.json` to version control
- Keep your API keys and credentials secure
- Use environment variables for sensitive information
- The `.gitignore` file is configured to exclude sensitive files

## Available Commands

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license] 