import subprocess
from pprint import pprint

# ToDo: may be make it as package

if __name__ == '__main__':
    # Two copies are not good. Currently, I do this because Docker doesn't allow access outside(level up) current folder

    code = subprocess.run(["python3","-m", "grpc_tools.protoc", "--proto_path=.", "--python_out=../Client", "--grpc_python_out=../Client", "service.proto"])
    if code.returncode != 0:
        pprint("Error during protobuf stub generation for client")

    code = subprocess.run(["python3","-m", "grpc_tools.protoc", "--proto_path=.", "--python_out=../Server", "--grpc_python_out=../Server", "service.proto"])
    if code.returncode != 0:
        pprint("Error during protobuf stub generation for server")
