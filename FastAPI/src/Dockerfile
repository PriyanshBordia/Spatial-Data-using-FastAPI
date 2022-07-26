FROM python:3.9.4-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_NAME spatial_data
ENV DB_USERNAME ""
ENV DB_PASSWORD ""
ENV DB_PORT 5432
ENV DB_HOST database

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python -m venv venv
RUN source /code/venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt & rm -rf /root/.cache/pip
RUN apk upgrade gdal
RUN apk upgrade geos

COPY ./app /code/app

CMD ["echo", "Hi, Captain.!"]
