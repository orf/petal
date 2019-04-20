import sys
import json

from google.protobuf.compiler import plugin_pb2
from google.protobuf.json_format import MessageToDict


def generate_service_metadata(request: plugin_pb2.CodeGeneratorRequest,
                              response: plugin_pb2.CodeGeneratorResponse):
    files = {f.name: f for f in request.proto_file}
    to_generate = {n: files[n] for n in request.file_to_generate}

    for name, fd in to_generate.items():

        services = {
            service.name: {
                method.name: {
                    'client_streaming': method.client_streaming,
                    'server_streaming': method.server_streaming
                }
                for method in service.method
            }
            for service in fd.service
        }

        if not services:
            continue

        output = response.file.add()
        output.insertion_point = 'module_scope'
        output.name = fd.name[:-6].replace('-', '_') + '_pb2.py'
        output.content = 'STREAMING_INFO = %s' % services
        print(f'Writing structure to {output.name}', file=sys.stderr)


def main():
    data = sys.stdin.buffer.read()
    request = plugin_pb2.CodeGeneratorRequest()
    request.ParseFromString(data)

    response = plugin_pb2.CodeGeneratorResponse()
    generate_service_metadata(request, response)
    output = response.SerializeToString()

    sys.stdout.buffer.write(output)


if __name__ == '__main__':
    main()
