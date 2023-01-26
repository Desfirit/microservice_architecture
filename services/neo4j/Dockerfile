FROM python:3.10.9-slim-bullseye

WORKDIR /app

RUN pip3 install flask
RUN pip3 install py2neo

COPY . .

CMD ["python3", "main.py"]