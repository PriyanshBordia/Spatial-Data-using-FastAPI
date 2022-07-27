FROM python:3.9.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_NAME spatial_data
ENV DB_USERNAME ""
ENV DB_PASSWORD ""
ENV DB_PORT 5432
ENV DB_HOST database

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install -r /usr/src/app/requirements.txt && rm -rf /root/.cache/pip
RUN apk add gdal
RUN apk add geos

COPY . /usr/src/app/

CMD ["echo", "Hi, Captain.!"]
# CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]
