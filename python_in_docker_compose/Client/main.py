import socket
from pprint import pprint
import signal
import sys

sock = None


def main():

    def int_handler(signum, frame):
        pprint("int_handler. recieved signal = {}".format(signum))
        if sock:
            pprint("Gracefully close socket")
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
        pprint("Can't connect. Error message is: {}".format(e) )
        exit(-1)

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    while True:

        try:
            # отправляем сообщение
            sock.send(bytes('Hello, world', encoding = 'UTF-8'))
        except Exception as e:
            pprint("Excepetion when send data = {}".format(e))
            break

        try:
            # читаем ответ от серверного сокета
            data = sock.recv(1024).decode('utf8')
        except Exception as e:
            pprint("Excepetion when recv data = {}".format(e))
            break
        #pprint(data)
        #sleep(1)

    # закрываем соединение
    sock.close()


if __name__ == "__main__":
    main()