FROM python

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_NAME spatial_data
ENV DB_USERNAME ""
ENV DB_PASSWORD ""
ENV DB_PORT 5432
ENV DB_HOST database
# ENV GDAL_LIBRARY_PATH /home/sue/local/lib/libgdal.so

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python -m venv venv
RUN source /code/venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

# && rm -rf /root/.cache/pip

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# CMD ["echo", "Hi, Captain.!"]