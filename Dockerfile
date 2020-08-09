FROM python:3.6-slim

RUN mkdir /project_name

COPY . /project_name

WORKDIR /project_name

# RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt