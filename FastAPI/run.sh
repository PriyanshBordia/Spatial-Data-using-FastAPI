#!/bin/sh
uvicorn src.app.main:app --reload --port 8002
# gunicorn main:app --workers 4 --worker-class uviconrn.workers.UvicornWorker --bind 0.0.0.0:80
