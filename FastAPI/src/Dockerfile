FROM python

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_NAME spatial_data
ENV DB_USERNAME priyansh
ENV DB_PASSWORD priyanshbordia
ENV DB_PORT 5432
ENV DB_HOST 127.0.0.1

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip && pip install -r /usr/src/app/requirements.txt && rm -rf /root/.cache/pip

COPY . /usr/src/app/

CMD ["echo", "Hi, Captain.!"]