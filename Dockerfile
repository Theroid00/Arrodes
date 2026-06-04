FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if any (none needed for this lightweight scraper bot)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Expose the keep-alive health check port (default Hugging Face Spaces port)
EXPOSE 7860

# Run the Discord bot
CMD ["python", "main.py"]
