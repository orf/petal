import functools
import contextvars
import grpc
from typing import Callable, List, get_type_hints, Type, NamedTuple, Dict, Iterable

from google.protobuf.message import Message

from .grpc_services import load_all_grpc_services, GRPCMethod, GRPCService
from .exceptions import MultipleServicesDefined, NoServicesDefined, AmbiguousMethod, IncorrectMethodArguments, \
    AmbiguousGRPCMethod
from . import log

context = contextvars.ContextVar('petal.context')

__all__ = ['Service']


class Handler(NamedTuple):
    name: str
    function: Callable
    input: Type
    output: Type

    @property
    def python_name(self):
        return self.function.__name__

    def create_method_handler(self) -> grpc.RpcMethodHandler:
        stream_input = hasattr(self.input, '__origin__') and issubclass(self.input.__origin__, Iterable)
        stream_output = hasattr(self.output, '__origin__') and issubclass(self.output.__origin__, Iterable)
        input_type = self.input if not stream_input else self.input.__args__[0]
        output_type = self.output if not stream_output else self.output.__args__[0]

        handlers = {
            (False, False): grpc.unary_unary_rpc_method_handler,
            (True, False): grpc.stream_unary_rpc_method_handler,
            (False, True): grpc.unary_stream_rpc_method_handler,
            (True, True): grpc.stream_stream_rpc_method_handler,
        }

        constructor = handlers[(stream_input, stream_output)]
        return constructor(
            self.function,
            request_deserializer=input_type.FromString,
            response_serializer=output_type.SerializeToString
        )


def camel_case_name(name):
    return ''.join(p.capitalize() for p in name.split('_'))


@functools.lru_cache()
def load_grpc_service(package, service_name=None) -> GRPCService:
    all_services = load_all_grpc_services(package)

    if not all_services:
        raise NoServicesDefined()

    if len(all_services) > 1:
        if not service_name:
            raise MultipleServicesDefined(all_services.keys())
        service = all_services[service_name]
    else:
        service = all_services[list(all_services.keys())[0]]

    return service


class Service:
    def __init__(self, package: str, service_name: str = None):
        self.package = package
        self.service_name = service_name
        self.rpc_methods: List[Handler] = []
        self.logger = log.logger

    def dispatch(self, request_object: Message, context_object: grpc.ServicerContext, func: Callable):
        ctx = contextvars.copy_context()
        context.set(context_object)

        bound_logger = self.logger.bind(peer=context_object.peer())

        with bound_logger.catch():
            try:
                return ctx.run(func, request_object)
            except exceptions.GRPCError as e:
                context_object.set_code(e.code)
                if e.details:
                    context_object.set_details(e.details)
            except NotImplementedError:
                context_object.set_code(grpc.StatusCode.UNIMPLEMENTED)

    def grpc(self, name: str = None):
        def inner(func):
            @functools.wraps(func)
            def wrapper(request_object, context_object):
                return self.dispatch(request_object, context_object, func)

            hints = get_type_hints(func)
            request_type = hints['request']
            return_type = hints['return']

            self.rpc_methods.append(
                Handler(
                    name=name or camel_case_name(func.__name__),
                    function=wrapper,
                    input=request_type,
                    output=return_type,
                )
            )

            return wrapper

        return inner

    def create_service_handler(self) -> 'grpc.ServiceRpcHandler':
        handlers = {
            method.name: method.create_method_handler()
            for method in self.rpc_methods
        }
        service = load_grpc_service(self.package, self.service_name)
        return grpc.method_handlers_generic_handler(
            service.full_name,
            handlers
        )

    def validate_service(self):
        service = load_grpc_service(self.package, self.service_name)
        method_name_mapping: Dict[str, GRPCMethod] = {method.name: method for method in service.methods}
        found_methods = set()

        for method in self.rpc_methods:
            if method.name not in method_name_mapping:
                raise AmbiguousMethod(method.name)
            grpc_method = method_name_mapping[method.name]
            # Check the types are correct
            input_type = grpc_method.input_type
            output_type = grpc_method.output_type

            if grpc_method.input_stream:
                input_type = Iterable[input_type]
            if grpc_method.output_stream:
                output_type = Iterable[output_type]

            if method.input != input_type:
                raise IncorrectMethodArguments(method.python_name, 'input', method.input, input_type)
            if method.output != output_type:
                raise IncorrectMethodArguments(method.python_name, 'output', method.output, output_type)
            found_methods.add(grpc_method)

        missing_methods = set(service.methods) - found_methods
        if missing_methods:
            raise AmbiguousGRPCMethod(name=list(missing_methods)[0].name)
