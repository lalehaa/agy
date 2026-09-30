FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and catalog
COPY app ./app
COPY static ./static
COPY catalog ./catalog
COPY data ./data
COPY agy_agent ./agy_agent

# Symlink catalog for root-level resolution
RUN ln -s /app/catalog /catalog

EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
