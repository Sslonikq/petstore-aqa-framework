FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


COPY pyproject.toml ./
COPY api api
COPY config config
COPY factories factories
COPY models models
COPY utils utils

RUN pip install --no-cache-dir -e .


COPY conftest.py ./
COPY tests tests

CMD ["pytest"]
