FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# curl is kept only for the container HEALTHCHECK below.
# build-essential/git were dropped: psycopg[binary] and every package in
# requirements.txt ship prebuilt wheels, so no compiler toolchain is needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# app.py, backend.py, tools/, templates/, static/ are copied above.
# .env is never copied into the image (see .dockerignore) — all secrets
# (GROQ_API_KEY, AVIATIONSTACK_API_KEY, TAVILY_API_KEY, DATABASE_URL, etc.)
# are injected at runtime via `docker run -e` / `--env-file` or your
# platform's environment variable settings (e.g. Render).

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Shell form so ${PORT} expands: Render (and similar platforms) inject a
# dynamic PORT env var at runtime; this falls back to 8000 for local
# `docker run` where PORT isn't set.
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}