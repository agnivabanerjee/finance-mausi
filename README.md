# Finance Mausi 🤖

An intelligent financial assistant powered by Anthropic's Claude and AlphaVantage, built with LangChain and Model Context Protocol (MCP).

## ✨ Features

- 🤖 Powered by Anthropic's Claude 3.5 Sonnet
- 📊 Real-time stock market data via AlphaVantage API
- 🔄 Intraday and daily stock price tracking
- 🛠️ MCP tools for seamless API integration
- 💬 User-friendly Gradio chat interface
- 🐳 Docker containerization for easy deployment

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance-mausi.git
cd finance-mausi
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Configure your `.env` file with required API keys:
```env
# Required
ANTHROPIC_API_KEY=your-anthropic-api-key
ALPHAVANTAGE_API_KEY=your-alphavantage-api-key

# Optional (for AWS features)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-east-1
```

4. Build and run with Docker:
```bash
docker compose up --build
```

5. Access the interface at `http://localhost:7860`

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| ANTHROPIC_API_KEY | Your Anthropic API key | Yes |
| ALPHAVANTAGE_API_KEY | Your AlphaVantage API key | Yes |
| AWS_ACCESS_KEY_ID | AWS Access Key | No |
| AWS_SECRET_ACCESS_KEY | AWS Secret Key | No |
| AWS_DEFAULT_REGION | AWS Region | No |
| DEBUG | Enable debug mode | No |
| LOG_LEVEL | Logging level | No |

## 🏗️ Architecture

The application is built using:
- LangChain for agent orchestration
- Anthropic's Claude 3.5 Sonnet for natural language processing
- AlphaVantage for financial data
- Model Context Protocol (MCP) for tool integration
- Gradio for the web interface
- Docker for containerization

## 💻 Development

To run the application locally without Docker:

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

## 🔒 Security Notes

- Never commit the `.env` file to version control
- Keep your API keys secure
- Use environment variables for sensitive information
- The `.gitignore` file is configured to exclude sensitive files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License

Copyright (c) 2024 Finance Mausi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 