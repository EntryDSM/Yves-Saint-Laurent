FROM python:3.7.3-slim-stretch AS base

MAINTAINER Shin Eunju <eunjuoi0515@gmail.com>

ENV VAULT_TOKEN $VAULT_TOKEN
ENV GITHUB_TOKEN $GITHUB_TOKEN
ENV RUN_ENV prod
ENV SERVICE_NAME ysl
ENV DATABASE_URL $DATABASE_URL
ENV JWT_SECRET_KEY $JWT_SECRET_KEY

COPY . .
WORKDIR .

RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    gcc

RUN pip install -r requirements.txt

CMD [".ysl/server.py"]
EXPOSE 80
ENTRYPOINT ["python"]
