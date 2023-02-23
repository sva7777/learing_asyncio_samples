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

RUN addgroup -S grpc_client && \
    adduser -S grpc_client -G grpc_client
USER grpc_client

FROM code as development


FROM development as debug
RUN pip3 install debugpy


