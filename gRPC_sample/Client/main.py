import sys, os
sys.path.insert(0, os.path.abspath('..'))

# ToDo: add logging
# ToDo: add SigINT handler and exceptions

import grpc
import service_pb2
import service_pb2_grpc

from pprint import pprint

if __name__ == '__main__':
    # ToDo: read port number from env variable
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.SimpleServiceStub(channel)

    # make a rRPC call
    request = service_pb2.StringRequest()
    request.request_id = 0
    request.message = "request"

    try:
        # ToDo: check timeout setting in gRPC
        while True:
            response = stub.ConvertToUpperCase(request, timeout=2)

            if response.request_id != request.request_id:
                # ToDo: make own Exception
                raise Exception("request_id in response {} is not same as request {}".format(response.request_id, request.request_id))

            request.request_id += 1

            # request_id is defined as uint32 in proto. Handle overflow
            if request.request_id == 4294967295:
                request.request_id = 0

    except grpc._channel._InactiveRpcError as ex:
        # ToDo: repeat request for 10 (make configurable) times, sleep 1 (make configurable) second
        # need to handle timeout
        # need to handle no connection

        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        pprint(message)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        pprint(message)








