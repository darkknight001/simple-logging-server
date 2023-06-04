FROM python:3.9

WORKDIR /app

COPY log_server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
