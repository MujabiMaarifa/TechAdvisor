# Use an official Python image
FROM python:3.13-slim

# Install SWI-Prolog
RUN apt-get update && \
    apt-get install -y swi-prolog && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "jaribu.py", "--server.port=8501", "--server.address=0.0.0.0"]

