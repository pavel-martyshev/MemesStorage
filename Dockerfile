FROM python:3.11-slim-bullseye

RUN mkdir /app

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app/

RUN python -m pip install -r requirements.txt

EXPOSE your_port
