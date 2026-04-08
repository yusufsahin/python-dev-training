FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Windows checkout'ta CRLF kırık shebang / exec hatasına yol açmasın
RUN sed -i 's/\r$//' docker-entrypoint.sh \
    && chmod +x docker-entrypoint.sh \
    && adduser --system --group --no-create-home app \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app \
    && chmod -R u+w /app/staticfiles /app/media

# adduser --no-create-home → /nonexistent; Gunicorn kontrol soketi vb. için yazılabilir HOME gerekir
ENV HOME=/app

USER app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "storium.wsgi:application"]
