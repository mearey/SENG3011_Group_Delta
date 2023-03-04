from concurrent import futures

import grpc
import server_pb2
import server_pb2_grpc
import WebScraper

class ServerTest(server_pb2_grpc.ServerTestServicer):
    def test(self, request, context):
        print("Got request " + str(request))
        return server_pb2.ServerOutput(message=str(WebScraper.GetDataType(request.dataType)))
    
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    server_pb2_grpc.add_ServerTestServicer_to_server(ServerTest(),server)
    server.add_insecure_port("[::]:50051")
    print("Server starting :D")
    server.start()
    server.wait_for_termination()

server()