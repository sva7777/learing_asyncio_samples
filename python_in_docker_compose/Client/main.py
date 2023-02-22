import socket
import signal
import time
import os

import logging
from sys import stdout


def main(server_host, port):

    def int_handler(signum, frame):
        logger.error("int_handler. Received signal = {}".format(signum))
        # ToDo: use different strategies for SIG_INT and SIG_TERM(more aggressive - close socket)
        if sock:
            nonlocal continue_working
            logger.error("Try to gracefully close socket")
            continue_working = False

    # создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set time out for connection(in seconds)
    sock.settimeout(20)

    logger.info("server_host: {}".format(server_host))
    logger.info("server_port: {}".format(port))


    # подключемся к серверному сокету
    try:
        sock.connect((server_host, port))
    except Exception as e:
        sock.close()
        logger.error("Can't connect. Error message is: {}".format(e) )
        exit(-1)

    # use this flag to stop calls to server
    continue_working = True

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    while continue_working:

        try:
            # отправляем сообщение
            sock.send(bytes('Hello, world', encoding = 'UTF-8'))
        except Exception as e:
            logger.error("Exception when send data = {}".format(e))
            break

        try:
            # читаем ответ от серверного сокета
            data = sock.recv(1024).decode('utf8')
        except Exception as e:
            logger.error("Exception when recv data = {}".format(e))
            break
        logger.debug(data)

        # ToDo: read value from env variable?
        time.sleep(0.5)

    # закрываем соединение
    sock.close()


if __name__ == "__main__":

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
        logger.setLevel(logging.WARNING)

    logFormatter = logging.Formatter \
        ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.info("Client is started")


    port = os.getenv('server_port')
    if not port:
        logger.warning("env variable server_port is not specified. 55000 is used" )
        port = 55000
    port = int(port)

    server_host = os.getenv('server_host')
    if not server_host:
        logger.warning("env variable server_host is not specified. localhost is used")
        server_host = "socket_server"


    main(server_host, port)

    logger.info("Exit client")