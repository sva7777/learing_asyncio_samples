import pika
import sys, os, time
import logging
from sys import stdout


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        logger.info(" [x] Received %r" % body)
        time.sleep(15)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=False)

    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


# ToDo: handle signals

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
        logger.info("Start Consumer")
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
