import socket
import signal
import time
import os

import logging
from sys import stdout

def main(server_host, port):

    def int_handler(signum, frame):
        logger.debug("int_handler. Received signal = {}".format(signum))
        if sock:
            logger.debug("Gracefully close socket")
            sock.close()
            exit(-1)

    # создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set time out for connection(in seconds)
    sock.settimeout(20)

    logger.debug("server_host: {}".format(server_host))
    logger.debug("server_port: {}".format(port))


    # подключемся к серверному сокету
    try:
        sock.connect((server_host, port))
    except Exception as e:
        sock.close()
        logger.debug("Can't connect. Error message is: {}".format(e) )
        exit(-1)

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    while True:

        try:
            # отправляем сообщение
            sock.send(bytes('Hello, world', encoding = 'UTF-8'))
        except Exception as e:
            logger.debug("Excepetion when send data = {}".format(e))
            break

        try:
            # читаем ответ от серверного сокета
            data = sock.recv(1024).decode('utf8')
        except Exception as e:
            logger.debug("Excepetion when recv data = {}".format(e))
            break
        logger.debug(data)
        time.sleep(0.1)

    # закрываем соединение
    sock.close()


if __name__ == "__main__":
    # Define logger
    logger = logging.getLogger('mylogger')

    logger.setLevel(logging.DEBUG)  # set logger level
    logFormatter = logging.Formatter \
        ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.debug("Client is started")

    port = os.getenv('server_port')
    if not port:
        logger.debug("env variable server_port is not specified. 55000 is used" )
        port = 55000
    port = int(port)

    server_host = os.getenv('server_host')
    if not server_host:
        logger.debug("env variable server_host is not specified. localhost is used")
        server_host = "localhost"

    main(server_host, port)

    logger.debug("Exit client")