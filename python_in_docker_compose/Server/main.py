import socket
import asyncio
import os
import signal
import functools


import logging
from sys import stdout

accept_log_file_name = "accept.log"

async def handle_client(client):
    loop = asyncio.get_event_loop()

    try:
        request = None

        # ToDo: request quit is not used currently
        while request != 'quit':
            try:
                request = (await loop.sock_recv(client, 255)).decode('utf8')
            except Exception as e:
                logger.error("Problem with sock_recv ={}".format(e))
                break

            if not request:
                logger.info("received EOF")
                break  # EOF - closed by client

            logger.debug("request = {}".format(request))
            response = request.upper()
            try:
                await loop.sock_sendall(client, response.encode('utf8'))
            except Exception as e:
                logger.error("Problem with sendall ={}".format(e))
                break

    except asyncio.CancelledError:
        logger.error("Courotine for hadle client {} was cancelled".format(client))

    logger.debug("Close socket")
    client.close()


async def shutdown(sig, loop):
    logger.error('Received signal {0}'.format(sig.name))

    # ToDo: use different strategies for SIG_INT and SIG_TERM(more aggressive - ?)

    tasks = [task for task in asyncio.all_tasks() if task is not
             asyncio.current_task()]
    list(map(lambda task: task.cancel(), tasks))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    logger.info('finished awaiting cancelled tasks, results: {0}'.format(results))
    loop.stop()


async def run_server(host, port, conn_count):

    # run_server is self courotine
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logger.info("hostname: {}".format(host))
        logger.info("port: {}".format(port))
        logger.info("conn_count: {}".format(conn_count))

        server.bind((host, port))
        server.listen(conn_count)
        server.setblocking(False)

        loop = asyncio.get_event_loop()

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig,
                                    functools.partial(asyncio.ensure_future,
                                                  shutdown(sig, loop)))

        while True:
            client, address = await loop.sock_accept(server)
            with open(accept_log_file_name,"a") as file:
                file.write("New client from address = {}\n".format(address))
            loop.create_task(handle_client(client))
    except asyncio.CancelledError:
        logger.error("Courotine run_server was cancelled")
        server.close()




if __name__ == "__main__":

    # ToDO: use uv_loop ? Currently I need ability to debug. Speed is not a question

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

    # Define logger
    logger = logging.getLogger('mylogger')

    try:
        logger.setLevel(logger_level)  # set logger level
    except Exception as e:
        logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter \
        ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.info("Start server")

    port = os.getenv('port_to_listen')
    if not port:
        logger.warning("env variable port_to_listen is not specified. 55000 is used" )
        port = 55000
    port= int(port)

    host = os.getenv('server_host')
    if not host:
        logger.warning("env variable server_host is not specified. localhost is used" )
        host = "localhost"


    conn_count = os.getenv('conn_count')
    if not conn_count:
        logger.warning("env variable conn_count is not specified. 10 is used" )
        conn_count = 10
    else:
        conn_count = int(conn_count)

    # clear log file if it exists
    if os.path.exists(accept_log_file_name):
        os.remove(accept_log_file_name)

    try:
        asyncio.run(run_server(host, port, conn_count))
    finally:
        logger.info("End of program")

