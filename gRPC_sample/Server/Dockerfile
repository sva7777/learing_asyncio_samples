FROM python:3.8-alpine as base
RUN mkdir /app
ADD requirements.txt /app
WORKDIR /app

CMD ["python","main.py"]

RUN pip3 install -r requirements.txt

FROM base as code

ADD main.py /app
ADD service_pb2_grpc.py /app
ADD service_pb2.py /app

RUN addgroup -S grpc_server && \
    adduser -S grpc_server -G grpc_server
USER grpc_server

FROM code as development


FROM development as debug
RUN pip3 install debugpy


