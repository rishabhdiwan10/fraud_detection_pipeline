# Use the official, lightweight Python 3.11 image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install the OpenMP C++ library required by XGBoost on Linux
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Copy the dependency list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API script and the trained model
COPY app.py .
COPY fraud_model.json .

# Expose the port GCP Cloud Run expects
EXPOSE 8080

# Command to run the high-performance Uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]