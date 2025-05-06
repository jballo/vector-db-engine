FROM python:3.11-slim AS builder
WORKDIR /app

# copy and install pinned deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim
LABEL org.opencontainers.image.source="https://github.com/jballo/vector-db-engine.git"
WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY app ./app

EXPOSE 8000
# uvicorn will serve app.main:app by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
