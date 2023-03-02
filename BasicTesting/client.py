import grpc
import sys

import server_pb2
import server_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = server_pb2_grpc.ServerTestStub(channel)
        response = stub.test(server_pb2.ClientInput(dataType = sys.argv[1]))
    print("client received: " + response.message)
run()