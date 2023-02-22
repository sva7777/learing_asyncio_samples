import subprocess
from pprint import pprint

# ToDo: may be make it as package to remove sys.path.insert trick

if __name__ == '__main__':
     code =subprocess.run(["python3","-m", "grpc_tools.protoc", "--proto_path=.", "--python_out=..", "--grpc_python_out=..", "service.proto"])
     if code.returncode != 0:
        pprint("Error during protobuf stub generation")
