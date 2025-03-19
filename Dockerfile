FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip
RUN pip install uv

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies using uv with --system flag
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a directory for logs
RUN mkdir -p /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 7860

# Start the MCP servers and Gradio app
CMD ["sh", "-c", "python servers/web_server.py > /app/logs/web_server.log 2>&1 & \
                  python servers/finance_server.py > /app/logs/finance_server.log 2>&1 & \
                  python servers/aws_server.py > /app/logs/aws_server.log 2>&1 & \
                  python agent.py"] 