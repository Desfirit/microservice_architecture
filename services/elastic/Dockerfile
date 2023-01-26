FROM python:3.10.9-slim-bullseye

WORKDIR /app

RUN pip3 install elasticsearch


COPY . .

CMD ["python3", "main.py"]