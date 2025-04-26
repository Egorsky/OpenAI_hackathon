# Start from official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose port (FastAPI default is 8080)
EXPOSE 8080

# Command to run the FastAPI app
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8080"]