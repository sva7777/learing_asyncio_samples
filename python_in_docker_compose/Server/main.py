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
                logger.debug("Problem with sock_recv ={}".format(e))
                break

            if not request:
                logger.debug("received EOF")
                break  # EOF - closed by client

            logger.debug("request = {}".format(request))
            response = request.upper()
            try:
                await loop.sock_sendall(client, response.encode('utf8'))
            except Exception as e:
                logger.debug("Problem with sendall ={}".format(e))
                break

    except asyncio.CancelledError:
        logger.debug("Courotine for hadle client {} was cancelled".format(client))

    logger.debug("Close socket")
    client.close()


async def shutdown(sig, loop):
    logger.debug('Received signal {0}'.format(sig.name))

    tasks = [task for task in asyncio.all_tasks() if task is not
             asyncio.current_task()]
    list(map(lambda task: task.cancel(), tasks))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    logger.debug('finished awaiting cancelled tasks, results: {0}'.format(results))
    loop.stop()


async def run_server():

    # run_server is self courotine
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ToDo: make host and port configurable from docker compose
        server.bind(('localhost', 55000))
        server.listen(10)
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
        logger.debug("Courotine run_server was cancelled")
        server.close()




if __name__ == "__main__":

    # Define logger
    logger = logging.getLogger('mylogger')

    logger.setLevel(logging.DEBUG)  # set logger level
    logFormatter = logging.Formatter \
        ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)


    logger.debug("Start server")

    # clear log file if it exists
    if os.path.exists(accept_log_file_name):
        os.remove(accept_log_file_name)

    try:
        asyncio.run(run_server())
    finally:
        logger.debug("End of program")

