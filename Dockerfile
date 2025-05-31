FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Expose the Flask port
EXPOSE 5000

# Use python run.py directly for better development experience
CMD ["python", "run.py"]