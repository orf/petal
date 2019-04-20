import pkgutil

import importlib
from typing import NamedTuple, List, Dict, Generator, Type
from types import ModuleType
from google.protobuf import symbol_database

pb_symbol_database = symbol_database.Default()


class GRPCMethod(NamedTuple):
    name: str
    full_name: str
    input_type: Type
    input_stream: bool
    output_type: Type
    output_stream: bool


class GRPCService(NamedTuple):
    name: str
    full_name: str
    methods: List[GRPCMethod]


def load_all_grpc_services(package: str) -> Dict[str, GRPCService]:
    services = {}

    for module in iter_modules(package):
        for service_name, service_descriptor in module.DESCRIPTOR.services_by_name.items():

            service = GRPCService(name=service_name,
                                  full_name=service_descriptor.full_name,
                                  methods=[])
            for method_descriptor in service_descriptor.methods:
                stream_info = module.STREAMING_INFO[service_name][method_descriptor.name]
                input_type = pb_symbol_database.GetSymbol(method_descriptor.input_type.full_name)
                output_type = pb_symbol_database.GetSymbol(method_descriptor.output_type.full_name)
                method = GRPCMethod(name=method_descriptor.name,
                                    full_name=method_descriptor.full_name,
                                    input_type=input_type,
                                    output_type=output_type,
                                    input_stream=stream_info['client_streaming'],
                                    output_stream=stream_info['server_streaming']
                                    )
                service.methods.append(method)
            services[service.name] = service

    return services


def iter_modules(package: str) -> Generator[ModuleType, None, None]:
    for module_info in pkgutil.iter_modules([f'{package}/protobuf']):
        if not module_info.name.endswith('_pb2'):
            continue
        yield importlib.import_module(f'{package}.protobuf.{module_info.name}')
