import functools
from typing import Callable, List, get_type_hints, Type, NamedTuple, Optional, Dict, Iterable
from .grpc_services import load_all_grpc_services, GRPCMethod, GRPCService
from .exceptions import MultipleServicesDefined, NoServicesDefined, AmbiguousMethod, IncorrectMethodArguments

__all__ = ['GRPCService']


class Handler(NamedTuple):
    name: str
    grpc_name: Optional[str]
    function: Callable
    input: Type
    output: Type


def camel_case_name(name):
    return ''.join(p.capitalize() for p in name.split('_'))


class Service:
    def __init__(self, package: str, service_name: str = None):
        self.package = package
        self.service_name = service_name
        self.rpc_methods: List[Handler] = []

    def grpc(self, name: str = None):
        def inner(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            hints = get_type_hints(func)
            request_type = hints['request']
            return_type = hints['return']

            self.rpc_methods.append(
                Handler(
                    name=func.__name__,
                    function=wrapper,
                    input=request_type,
                    output=return_type,
                    grpc_name=name or camel_case_name(func.__name__)
                )
            )

            return wrapper

        return inner

    def create_server(self):
        pass

    def load_grpc_service(self) -> GRPCService:
        all_services = load_all_grpc_services(self.package)

        if not all_services:
            raise NoServicesDefined()

        if len(all_services) > 1:
            if not self.service_name:
                raise MultipleServicesDefined(all_services.keys())
            service = all_services[self.service_name]
        else:
            service = all_services[list(all_services.keys())[0]]

        return service

    def validate_service(self):
        service = self.load_grpc_service()
        method_name_mapping: Dict[str, GRPCMethod] = {method.name: method for method in service.methods}

        for method in self.rpc_methods:
            if method.grpc_name not in method_name_mapping:
                raise AmbiguousMethod(method.name)
            grpc_method = method_name_mapping[method.grpc_name]
            # Check the types are correct
            input_type = grpc_method.input_type
            output_type = grpc_method.output_type

            if grpc_method.input_stream:
                input_type = Iterable[input_type]
            if grpc_method.output_stream:
                output_type = Iterable[output_type]

            if method.input != input_type:
                raise IncorrectMethodArguments(method.name, 'input', method.input, input_type)
            if method.output != output_type:
                raise IncorrectMethodArguments(method.name, 'output', method.output, output_type)
