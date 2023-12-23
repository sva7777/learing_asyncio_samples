from confluent_kafka import Consumer
import logging, os
from sys import stdout
import signal


def main(c):

    def int_handler(signum, frame):
        nonlocal continue_working
        logger.error("int_handler. Received signal = {}".format(signum))
        # ToDo: use different strategies for SIG_INT and SIG_TERM(more aggressive ?)
        logger.error("stop consumer")
        continue_working = False

    # use this flag to stop consumer
    continue_working = True

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    while continue_working:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            logger.error("Error: {}".format(msg.error()))
            continue
        data = msg.value().decode("utf-8")
        logger.info(data)
    c.close()


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

    ################
    # ToDo: make consumer group configurable
    c = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "python-consumer-2",
            "auto.offset.reset": "earliest",
        }
    )
    logger.info("Available topics to consume: ", c.list_topics().topics)

    c.subscribe(["user-tracker"])

    ################

    main(c)
