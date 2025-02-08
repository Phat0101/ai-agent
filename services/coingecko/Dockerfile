FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Default port 
ENV PORT=8001

# Expose the port
EXPOSE ${PORT}

# Run the service
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"] 