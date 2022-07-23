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

RUN pip install --upgrade pip==22.2 \
	&& pip install virtualenv==20.15.1 \
	&& python -m venv venv \
	&& source venv/bin/activate \
	&& pip install --no-cache -r /usr/src/app/requirements.txt && rm -rf /root/.cache/pip

COPY . /usr/src/app/

# CMD ["echo", "Hi, Captain.!"]
