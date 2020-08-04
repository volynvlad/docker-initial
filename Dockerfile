FROM python:3.6-slim

RUN mkdir /project_name

COPY . /project_name

WORKDIR /project_name

RUN pip install -r requirements.txt