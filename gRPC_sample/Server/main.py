import time
from pprint import pprint

import sys, os
sys.path.insert(0, os.path.abspath('..'))

# ToDo: add logging
# ToDo: add SigINT handler and exceptions

import concurrent.futures as futures

import grpc
import service_pb2
import service_pb2_grpc


class SimpleServiceImplementation(service_pb2_grpc.SimpleServiceServicer):
    def ConvertToUpperCase(self, request, context):
        pprint("request ={}".format(request))
        pprint("context ={}".format(context))
        sr= service_pb2.StringResponse()
        sr.request_id = request.request_id
        sr.message = "Response"
        time.sleep(5)
        return sr

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SimpleServiceServicer_to_server(
        SimpleServiceImplementation(), server)

    # ToDo: make port configarable
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


