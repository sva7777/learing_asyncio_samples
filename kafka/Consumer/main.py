import time
from confluent_kafka import Consumer

################

#ToDo: make consumer group configurable

# Manually commit messages
c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest', 'enable.auto.commit': 'false'} )

print('Available topics to consume: ', c.list_topics().topics)

c.subscribe(['user-tracker'])


################

def main():
    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(data)

        # break program execution during this time to test functionality of __consumer_offsets
        time.sleep(5)

        #Manually commit messages
        c.commit(msg)
    c.close()


if __name__ == '__main__':
    main()
