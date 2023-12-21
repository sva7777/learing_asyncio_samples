import signal
import functools
import asyncio
import grpc
import logging
from sys import stdout

import sys, os

import service_pb2
import service_pb2_grpc


class SimpleServiceImplementation(service_pb2_grpc.SimpleServiceServicer):
    async def ConvertToUpperCase(self, request, context):
        logger.debug("request ={}".format(request))
        sr = service_pb2.StringResponse()
        sr.request_id = request.request_id
        sr.message = "Response"
        return sr


async def shutdown(sig, loop):
    logger.error("Received signal {0}".format(sig.name))

    # ToDo: use different strategies for SIG_INT and SIG_TERM(more aggressive - ?)

    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    list(map(lambda task: task.cancel(), tasks))
    results = await asyncio.gather(*tasks, return_exceptions=True)

    logger.info("finished awaiting cancelled tasks, results: {0}".format(results))
    loop.stop()


async def serve(host, port):
    try:
        server = grpc.aio.server()

        service_pb2_grpc.add_SimpleServiceServicer_to_server(
            SimpleServiceImplementation(), server
        )

        logger.info("server_host: {}".format(host))
        logger.info("port: {}".format(port))

        # ToDo in this place can be exception if port is occupied
        server.add_insecure_port("{}:{}".format(server_host, port))

        loop = asyncio.get_event_loop()

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig, functools.partial(asyncio.ensure_future, shutdown(sig, loop))
            )
        await server.start()

        await server.wait_for_termination()
    except asyncio.CancelledError:
        logger.error("Courotine serve was cancelled")
        server.stop(None)


if __name__ == "__main__":
    # ToDO: use uv_loop ? Currently I need ability to debug. Speed is not a question
    debug_port = os.getenv("debug_port")
    if debug_port:
        import debugpy

        debugpy.listen(("0.0.0.0", int(debug_port)))

        wait_for_debuger_connection = os.getenv("wait_for_debuger_connection")
        if wait_for_debuger_connection and int(wait_for_debuger_connection) != 0:
            debugpy.wait_for_client()

    logger_level = os.getenv("logger_level")
    if not logger_level:
        logger_level = logging.DEBUG
    else:
        # check is user specified int debug_level. If so convert string to int
        try:
            logger_level = int(logger_level)
        except ValueError:
            # It seems log level set by full name. Do nothing
            pass

    # Define logger
    logger = logging.getLogger("mylogger")
    try:
        logger.setLevel(logger_level)  # set logger level
    except ValueError  as e:
        logger.setLevel(logging.DEBUG)
        logger.error("Error {} of setting log level = {}".format(e, logger_level))
        logger.warning("use logging level == DEBUG")


    logFormatter = logging.Formatter(
        "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
    )
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.info("Start server")

    port = os.getenv("port_to_listen")
    if not port:
        logger.warning("env variable port_to_listen is not specified. 50051 is used")
        port = 50051
    port = int(port)

    server_host = os.getenv("server_host")
    if not server_host:
        logger.warning("env variable server_host is not specified. localhost is used")
        server_host = "localhost"

    try:
        asyncio.run(serve(server_host, port))
    finally:
        logger.info("End of program")
