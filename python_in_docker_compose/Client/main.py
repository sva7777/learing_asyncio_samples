import socket
import signal
import time

import logging
from sys import stdout

def main():

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

    # подключемся к серверному сокету
    try:
        sock.connect(('localhost', 55000))
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

    main()

    logger.debug("Exit client")