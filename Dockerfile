# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN python -m spacy download en
RUN python -m spacy download de

COPY . .

ENTRYPOINT ["python", "cli.py"]