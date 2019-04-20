from typing import Iterable

from petal import Service
from example.protobuf.greeter_pb2 import HelloReply
from petal.protobuf.base_pb2 import HelloRequest

service = Service(__name__)


@service.grpc()
def say_hello(request: HelloRequest) -> HelloReply:
    pass


@service.grpc()
def say_hello_stream(request: Iterable[HelloRequest]) -> HelloReply:
    pass


@service.grpc()
def say_hello_response_stream(request: HelloRequest) -> Iterable[HelloReply]:
    pass


@service.grpc()
def say_hello_double_stream(request: Iterable[HelloRequest]) -> Iterable[HelloReply]:
    pass
