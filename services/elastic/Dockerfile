FROM python:3.10.9-slim-bullseye

WORKDIR /app

RUN pip3 install elasticsearch
RUN pip3 install elasticsearch_dsl
RUN pip3 install flask

COPY . .

CMD ["python3", "main.py"]