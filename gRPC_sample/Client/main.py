import signal
import grpc
import logging
from sys import stdout

import sys, os

import service_pb2
import service_pb2_grpc


class ControlValueMismatchException (Exception):
    pass


def main (host, port):
    def int_handler(signum, frame):
        nonlocal continue_working
        logger.error("int_handler. Received signal = {}".format(signum))
        logger.error("Try to gracefully close socket")
        continue_working = False


    # use this flag to stop calls to server
    continue_working = True

    logger.info("server_host: {}".format(host))
    logger.info("server_port: {}".format(port))

    channel = grpc.insecure_channel('{}:{}'.format(host,port))

    stub = service_pb2_grpc.SimpleServiceStub(channel)

    # make a rRPC call
    request = service_pb2.StringRequest()
    request.request_id = 0
    request.message = "request"

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    try:

        while continue_working:
            logger.debug("request_id is ={}".format(request.request_id))
            # ToDo: make timeout configurable from evn variables
            response = stub.ConvertToUpperCase(request, timeout=2)

            if response.request_id != request.request_id:
                raise ControlValueMismatchException("request_id in response {} is not same as request {}".format(response.request_id, request.request_id))

            request.request_id += 1

            # request_id is defined as uint32 in proto. Handle overflow
            if request.request_id == 4294967295:
                request.request_id = 0

    except grpc._channel._InactiveRpcError as ex:
        # ToDo: repeat request for 10 (make configurable) times, sleep 1 (make configurable) second
        # handle timeout
        # handle no connection

        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.error(message)
    except ControlValueMismatchException as ex:
        logger.error(ex)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.error(message)



if __name__ == '__main__':
    debug_port = os.getenv('debug_port')
    if debug_port:
        import debugpy
        debugpy.listen(("0.0.0.0", int(debug_port)))

        wait_for_debuger_connection = os.getenv('wait_for_debuger_connection')
        if wait_for_debuger_connection and int(wait_for_debuger_connection) != 0:
            debugpy.wait_for_client()

    logger_level = os.getenv('logger_level')
    if not logger_level:
        logger_level = logging.DEBUG
    else:
        # int and string are supported as log level. Convert string(from evn var) to int if necessary
        try:
            logger_level = int(logger_level)
        except Exception:
            # It seems log level set by full name
            pass

    # Define logger
    logger = logging.getLogger('mylogger')

    try:
        logger.setLevel(logger_level)  # set logger level
    except Exception as e:
        logger.setLevel(logging.DEBUG)
        logger.error("Error {} of setting log level = {}".format(e,logger_level))


    logFormatter = logging.Formatter \
        ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.info("Client is started")

    port = os.getenv('server_port')
    if not port:
        logger.warning("env variable server_port is not specified. 50051 is used" )
        port = 50051
    port = int(port)

    server_host = os.getenv('server_host')
    if not server_host:
        logger.warning("env variable server_host is not specified. localhost is used")
        server_host = "localhost"

    main(server_host, port)

    logger.info("Exit client")








