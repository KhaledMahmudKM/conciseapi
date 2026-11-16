"""Chapter 12: gRPC client. Start server.py first, then:  python client.py"""
import grpc

import library_pb2
import library_pb2_grpc

with grpc.insecure_channel("127.0.0.1:50051") as channel:
    stub = library_pb2_grpc.LibraryStub(channel)

    book = stub.GetBook(library_pb2.GetBookRequest(id=3), timeout=2)    # always set a deadline
    print("unary:", book.title, book.year)

    for b in stub.ListBooks(library_pb2.ListBooksRequest(author="Jane Austen"), timeout=2):
        print("streamed:", b.title)

    try:
        stub.GetBook(library_pb2.GetBookRequest(id=99), timeout=2)
    except grpc.RpcError as err:
        print("error:", err.code().name, "-", err.details())

    print("wire size of one Book message:", len(book.SerializeToString()), "bytes")
