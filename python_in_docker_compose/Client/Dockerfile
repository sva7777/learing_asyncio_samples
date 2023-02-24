FROM python:3.8-alpine as base
RUN mkdir /app
ADD main.py /app
WORKDIR /app
CMD ["python","main.py"]

RUN addgroup -S socket_client && \
    adduser -S socket_client -G socket_client
USER socket_client


FROM base as debug
RUN pip3 install debugpy

FROM base as development

