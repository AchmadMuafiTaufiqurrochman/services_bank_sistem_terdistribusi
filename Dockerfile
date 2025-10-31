# Gunakan image Python ringan
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependensi sistem (client MySQL, gcc, dsb)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Salin requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode proyek
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8081

EXPOSE 8081

# Jalankan FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
