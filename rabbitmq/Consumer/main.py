import pika
import sys, os, time
import logging
from sys import stdout
import signal

def main():
    def int_handler(signum, frame):
        nonlocal continue_working
        logger.error("int_handler. Received signal = {}".format(signum))
        # ToDo: use different strategies for SIG_INT and SIG_TERM(more aggressive - ?)
        logger.error("stop receiving messages")
        continue_working = False

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    # use this flag to stop reading messages
    continue_working = True

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    # ToDo: switch to async implementation
    while continue_working:

        method_frame, header_frame, body = channel.basic_get('hello')
        if method_frame:
            logger.info(" [x] Received %r" % body)
            channel.basic_ack(method_frame.delivery_tag)



if __name__ == "__main__":
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
    except ValueError as e:
        logger.setLevel(logging.DEBUG)
        logger.error("Error {} of setting log level = {}".format(e, logger_level))
        logger.warning("use logging level == DEBUG")

    logFormatter = logging.Formatter(
        "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
    )

    consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.info("Start consumer")
    main()
    logger.info("Stop consumer")
