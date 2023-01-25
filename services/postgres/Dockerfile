FROM python:3.10.9-slim-bullseye

WORKDIR /app

RUN pip3 install flask

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2

COPY . .

CMD ["python3", "main.py"]