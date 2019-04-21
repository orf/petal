# :hibiscus: Petal - Flask, for gRPC services.

Petal reduces the boilerplate required to write and maintain gRPC based services whilst ensuring your service 
code is always in sync with your definitions. It aims to be a somewhat opinionated gRPC framework. 
**This is very, very early code**.

## Installation and features

`pip install petal`

Right now:

- [x] Define your service methods as simple Python functions
- [x] Ensure they are up to date with service definitions by utilizing type annotations
- [x] Build your proto definitions and run your app with a `petal` command
- [x] Share compiled protobuf definitions as Python packages.
- [x] Streaming requests and responses

Future features:

- [ ] Autoreloading during development
- [ ] Structured logging
- [ ] Some form of plugin architecture
- [ ] Distributed tracing
- [ ] A testing client
- [ ] AsyncIO support

## Hello world example:

```python
from petal import Service
from example.protobuf.greeter_pb2 import HelloReply, HelloRequest

service = Service(__name__)

@service.grpc()
def say_hello(request: HelloRequest) -> HelloReply:
    return HelloReply(message=f'Hello {request.name}')
```

## Tutorial: Creating a petal app

Lets create a Hello World Petal app. First lets define an entirely useless service. Place the file below 
in `hello_world/protobuf/service.proto`:

```proto
syntax = "proto3";
package hello_world.protobuf.service;

service HelloWorld {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
}

message HelloReply {
}
```

Then run `petal build hello_world`.

 
 Next, write our service definitions. Create a 
`hello_world/__init__.py` file and add some imports:

```python
from petal import Service
from hello_world.protobuf.service_pb2 import HelloReply, HelloRequest

service = Service(__name__)
```

This imports the request and response types our service will need. Next we need to fill in the 
`SayHello` method:

```python
@service.grpc()
def say_hello(request: HelloRequest) -> HelloReply:
    return HelloReply()
```

And finally, run the service by executing `petal run hello_world`. 

Now if we modify the service by adding a new method:

```proto
message HelloAgain {}

service HelloWorld {
  rpc SayHelloAgain (HelloRequest) returns (HelloAgain) {}
}
```

And run `petal build hello_world && petal run hello_world`, we get an error:

```shell
$ petal run hello_world
Error: Cannot find a suitable method for GRPC method SayHelloAgain
Please ensure one exists in your service code, or use service.grpc(name=NAME) to define one.
```

Petal is ensuring we have the correct Python methods defined for all our service functions. We can fix this 
by defining one:

```python
from hello_world.protobuf.service_pb2 import HelloAgain

@service.grpc()
def say_hello_again(request: HelloRequest) -> HelloAgain:
    return HelloAgain()
```

Now running `petal serve hello_world` will work.
