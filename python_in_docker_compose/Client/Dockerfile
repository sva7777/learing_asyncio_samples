FROM python:3.8-alpine as base
RUN mkdir /app
ADD main.py /app
WORKDIR /app
CMD ["python","main.py"]

FROM base as debug
RUN pip3 install debugpy

FROM base as development

