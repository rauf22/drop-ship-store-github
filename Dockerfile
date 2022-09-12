FROM python:3.6-alpine
WORKDIR /drop-ship-store-github
COPY ./ /drop-ship-store-github
RUN apk update && pip install -r /drop-ship-store-github/requirements.txt --no-cache-dir
EXPOSE 8000
CWD ["python", "manage.py", "runserver", "0.0.0.0:8000"]