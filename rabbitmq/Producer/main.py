import pika
import datetime

# ToDo: handle signals
# ToDo: get confirmation from RabbitMQ

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

print(" [x] Sent 'Hello World!'")

connection.close()
