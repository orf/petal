from typing import Iterable, Any

from grpc import StatusCode


class InitializationException(Exception):
    pass


class MultipleServicesDefined(InitializationException):
    def __init__(self, service_names: Iterable[str]):
        self.service_names = service_names

    def __str__(self):
        return f'Multiple GRPC services are defined. ' \
            f'Please use Service(..., service_name=NAME) to specify one.\n' \
            f'Services found: {", ".join(self.service_names)}.'


class NoServicesDefined(InitializationException):
    def __str__(self):
        return 'No services are defined. ' \
               'Please ensure one exists in your protobuf file.'


class AmbiguousMethod(InitializationException):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'Cannot find a suitable GRPC method for function {self.name}\n' \
            f'Please ensure one exists in your .proto file, or use service.grpc(name=NAME) ' \
            f'to define one.'


class AmbiguousGRPCMethod(InitializationException):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'Cannot find a suitable method for GRPC method {self.name}\n' \
            f'Please ensure one exists in your service code, or use service.grpc(name=NAME) ' \
            f'to define one.'



class IncorrectMethodArguments(InitializationException):
    def __init__(self, method_name: str, argument: str, given: Any, expected: Any):
        self.method_name = method_name
        self.argument = argument
        self.given = given
        self.expected = expected

    def __str__(self):
        return f'Method {self.method_name} has an incorrect {self.argument} \n' \
            f'Expected {self.expected}, found {self.given}.\n' \
            f'Please update your service definitions to ensure the types are correct.'


class GRPCError(Exception):
    code = None
    details = ""

    def __init__(self, details=None, code=None):
        if code:
            self.code = code
        if details:
            self.details = details


class Cancelled(GRPCError):
    code = StatusCode.CANCELLED


class InvalidArgument(GRPCError):
    code = StatusCode.INVALID_ARGUMENT


class DeadlineExceeded(GRPCError):
    code = StatusCode.DEADLINE_EXCEEDED


class NotFound(GRPCError):
    code = StatusCode.NOT_FOUND


class AlreadyExists(GRPCError):
    code = StatusCode.NOT_FOUND


class PermissionDenied(GRPCError):
    code = StatusCode.PERMISSION_DENIED


class Unauthenticated(GRPCError):
    code = StatusCode.UNAUTHENTICATED


class ResourceExhausted(GRPCError):
    code = StatusCode.RESOURCE_EXHAUSTED


class FailedPrecondition(GRPCError):
    code = StatusCode.FAILED_PRECONDITION


class Aborted(GRPCError):
    code = StatusCode.ABORTED


class Unimplemented(GRPCError):
    code = StatusCode.UNIMPLEMENTED


class InternalError(GRPCError):
    code = StatusCode.INTERNAL


class Unavailable(GRPCError):
    code = StatusCode.UNAVAILABLE


class DataLoss(GRPCError):
    code = StatusCode.DATA_LOSS
