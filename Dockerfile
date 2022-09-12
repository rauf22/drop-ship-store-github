FROM python:3.8.13-slim-buster
WORKDIR /drop-ship-store-github
COPY ./ /drop-ship-store-github
RUN apt update && python -m pip install --upgrade pip && pip install -r /drop-ship-store-github/requirements.txt --no-cache-dir
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]