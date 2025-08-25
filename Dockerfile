# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app/

# Make start.sh executable
RUN chmod +x /app/start.sh

# Expose FastAPI port
EXPOSE 8000


RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Use start.sh to run the app
CMD ["sh", "/app/start.sh"]
