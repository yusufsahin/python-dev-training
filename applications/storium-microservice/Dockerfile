FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini alembic.ini
COPY alembic/ alembic/
COPY app/ app/

COPY docker-entrypoint.sh .
RUN sed -i 's/\r$//' docker-entrypoint.sh \
    && chmod +x docker-entrypoint.sh \
    && adduser --system --group --no-create-home app \
    && chown -R app:app /app \
    && chmod -R u+w /app

ENV HOME=/app
USER app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
