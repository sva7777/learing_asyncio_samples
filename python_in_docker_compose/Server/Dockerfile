FROM python:3.8-alpine as base
RUN mkdir /app
ADD main.py /app
WORKDIR /app
CMD ["python","main.py"]

RUN addgroup -S socket_server && \
    adduser -S socket_server -G socket_server
USER socket_server


FROM base as debug
RUN pip3 install debugpy

FROM base as development