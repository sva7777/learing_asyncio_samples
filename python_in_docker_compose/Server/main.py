import socket
import asyncio
import os
from pprint import pprint

# ToDo: this code will be user inside docker container,
#  so need to handle SIG_TERM signal

accept_log_file_name = "accept.log"



async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None

    while request != 'quit':
        try:
            request = (await loop.sock_recv(client,255)).decode('utf8')
        except Exception as e:
            pprint("Problem with sock_recv ={}".format(e))
            pprint("close connection")
            break

        if not request:
            pprint("close socket because of EOF")
            break  # EOF - closed by client

        pprint("request = {}".format(request))
        response= request.upper()
        try:
            await loop.sock_sendall(client, response.encode('utf8'))
        except Exception as e:
            pprint("Problem with sendall ={}".format(e))
            pprint("close connection")
            break

    pprint("Close socket")
    client.close()

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('localhost', 55000))
    server.listen(10)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, address = await loop.sock_accept(server)
        with open(accept_log_file_name,"a") as file:
            file.write("New client from address = {}\n".format(address))
        loop.create_task(handle_client(client))



if os.path.exists(accept_log_file_name):
  os.remove(accept_log_file_name)

asyncio.run(run_server())