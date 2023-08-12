FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

COPY . .
