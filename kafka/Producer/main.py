from confluent_kafka import Producer
from faker import Faker
import json
import logging, os
import random
from sys import stdout
import signal

fake = Faker()


p = Producer({"bootstrap.servers": "localhost:9092"})


#####################


def receipt(err, msg):
    if err:
        print("Error: {}".format(err))
    else:
        message = "Produced message on topic {} with value of {}\n".format(
            msg.topic(), msg.value().decode("utf-8")
        )
        logger.info(message)
        print(message)


#####################
print("Kafka Producer has been initiated...")

# ToDo: handle signals and other interrupts


def main():
    def int_handler(signum, frame):
        nonlocal continue_working
        logger.error("int_handler. Received signal = {}".format(signum))
        # ToDo: use different strategies for SIG_INT and SIG_TERM(more aggressive ?)
        logger.error("stop sending messages")
        continue_working = False

    # use this flag to stop producer
    continue_working = True

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    for i in range(100):
        if continue_working == False:
            break

        data = {
            "user_id": fake.random_int(min=20000, max=100000),
            "user_name": fake.name(),
            "user_address": fake.street_address()
            + " | "
            + fake.city()
            + " | "
            + fake.country_code(),
            "platform": random.choice(["Mobile", "Laptop", "Tablet"]),
            "signup_at": str(fake.date_time_this_month()),
        }
        m = json.dumps(data)
        p.poll(1)
        p.produce("user-tracker", m.encode("utf-8"), callback=receipt)
        p.flush()



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

    main()
