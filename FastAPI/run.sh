#!/bin/sh
uvicorn main:app --reload
# gunicorn main:app --workers 4 --worker-class uviconrn.workers.UvicornWorker --bind 0.0.0.0:80