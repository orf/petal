from typing import Iterable

from petal import Service
from example.protobuf.greeter_pb2 import HelloReply
from petal.protobuf.base_pb2 import HelloRequest

service = Service(__name__)


@service.grpc()
def say_hello(request: HelloRequest) -> HelloReply:
    return HelloReply(message=f'Hello {request.name}')


@service.grpc()
def say_hello_stream(request: Iterable[HelloRequest]) -> HelloReply:
    names = [
        r.name
        for r in request
    ]
    return HelloReply(message=f'Hello {names}')


@service.grpc()
def say_hello_response_stream(request: HelloRequest) -> Iterable[HelloReply]:
    for i in range(4):
        yield HelloReply(message=f'Hello {request.name} ({i})')


@service.grpc()
def say_hello_double_stream(request: Iterable[HelloRequest]) -> Iterable[HelloReply]:
    names = [
        r.name
        for r in request
    ]
    for i in range(4):
        yield HelloReply(message=f'Hello {names} ({i})')
