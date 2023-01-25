FROM python:3.10.9-bullseye

WORKDIR /app

COPY requirements.mger ./

RUN pip3 install -r requirements.mger

COPY . .

CMD ["python3", "main.py"]