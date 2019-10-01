FROM python:3.7-alpine

MAINTAINER Shin Eunju <eunjuoi0515@gmail.com>

ENV VAULT_TOKEN $VAULT_TOKEN
ENV GITHUB_TOKEN $GITHUB_TOKEN
ENV RUN_ENV prod
ENV SERVICE_NAME ysl

COPY . .
WORKDIR .

RUN pip install -r requirements_dev.txt

CMD ["-m", "ysl"]
EXPOSE 80
ENTRYPOINT ["python"]

