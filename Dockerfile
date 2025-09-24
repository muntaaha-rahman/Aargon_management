FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install with timeout and retry settings
RUN pip install --no-cache-dir --timeout 100 --retries 5 -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["sh", "start.sh"]