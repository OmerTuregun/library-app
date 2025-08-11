FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
# TLS ve saat dilimi verileri (HTTPS için gerekli)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates tzdata \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
