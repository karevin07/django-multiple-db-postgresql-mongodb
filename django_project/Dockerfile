FROM python:3.8

ARG WORKSPACE='/home/workspace'
RUN mkdir -p ${WORKSPACE}
WORKDIR ${WORKSPACE}

COPY ./django_project/requirement.txt .

RUN pip install -r requirement.txt