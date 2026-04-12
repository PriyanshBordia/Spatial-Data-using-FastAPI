FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils libgdal-dev libgeos-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt && \
    groupadd -r app && useradd -r -g app app

COPY . /usr/src/app/

RUN chown -R app:app /usr/src/app
USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
