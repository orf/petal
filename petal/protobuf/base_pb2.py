# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: petal/protobuf/base.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='petal/protobuf/base.proto',
  package='petal.protobuf.base',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x19petal/protobuf/base.proto\x12\x13petal.protobuf.base\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\tb\x06proto3')
)




_HELLOREQUEST = _descriptor.Descriptor(
  name='HelloRequest',
  full_name='petal.protobuf.base.HelloRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='petal.protobuf.base.HelloRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=78,
)

DESCRIPTOR.message_types_by_name['HelloRequest'] = _HELLOREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HelloRequest = _reflection.GeneratedProtocolMessageType('HelloRequest', (_message.Message,), dict(
  DESCRIPTOR = _HELLOREQUEST,
  __module__ = 'petal.protobuf.base_pb2'
  # @@protoc_insertion_point(class_scope:petal.protobuf.base.HelloRequest)
  ))
_sym_db.RegisterMessage(HelloRequest)


# @@protoc_insertion_point(module_scope)
