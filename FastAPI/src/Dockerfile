FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DB_NAME=spatial_data
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=postgres
ENV DB_PORT=5432
ENV DB_HOST=database

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils libgdal-dev libgeos-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
