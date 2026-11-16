"""Chapter 12: gRPC server. Generate the stubs first (see library.proto), then:  python server.py"""
from concurrent import futures

import grpc

import library_pb2
import library_pb2_grpc

BOOKS = [
    library_pb2.Book(id=1, title="Pride and Prejudice", author="Jane Austen", year=1813),
    library_pb2.Book(id=2, title="Emma", author="Jane Austen", year=1815),
    library_pb2.Book(id=3, title="Dune", author="Frank Herbert", year=1965),
]


class Library(library_pb2_grpc.LibraryServicer):
    def GetBook(self, request, context):
        for book in BOOKS:
            if book.id == request.id:
                return book
        context.abort(grpc.StatusCode.NOT_FOUND, f"Book {request.id} does not exist")

    def ListBooks(self, request, context):
        for book in BOOKS:
            if not request.author or book.author == request.author:
                yield book


def serve(port: int = 50051) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    library_pb2_grpc.add_LibraryServicer_to_server(Library(), server)
    server.add_insecure_port(f"127.0.0.1:{port}")      # plaintext for the lab; use TLS in production
    server.start()
    return server


if __name__ == "__main__":
    print("gRPC server on 127.0.0.1:50051")
    serve().wait_for_termination()
