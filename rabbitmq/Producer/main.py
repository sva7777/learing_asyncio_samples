import pika
import datetime
import sys, os
import logging
from sys import stdout

# ToDo: handle signals
# ToDo: get confirmation from RabbitMQ


def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    # set up expire
    now = datetime.datetime.now()
    expire = 1000 * int((now.replace(minute=now.minute + 1) - now).total_seconds())


    channel.basic_publish(
        exchange="",
        routing_key="hello",
        body="Hello World!",
        properties=pika.BasicProperties(
            # job expiration (milliseconds from now), must be string, handled by rabbitmq)
            expiration=str(expire)
        ),
    )

    logger.info(" [x] Sent 'Hello World!'")

    connection.close()


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

    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
