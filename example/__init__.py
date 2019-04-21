from typing import Iterable

from petal import Service
from example.protobuf.greeter_pb2 import HelloReply, HelloRequest

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
    return HelloReply(message=", ".join(f'Hello {name}' for name in names))
