# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SmsPb.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from lib.pb_src.python_native import BaseResult_pb2
from lib.pb_src.python_native import BaseHeader_pb2

DESCRIPTOR = _descriptor.FileDescriptor(
  name='SmsPb.proto',
  package='Sms',
  serialized_pb=_b('\n\x0bSmsPb.proto\x12\x03Sms\x1a\x10\x42\x61seResult.proto\x1a\x10\x42\x61seHeader.proto\"z\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x0f\n\x07operate\x18\x02 \x02(\t\x12\x12\n\nverifycode\x18\x03 \x01(\t\x12\x0c\n\x04sign\x18\x04 \x02(\t\x12\x14\n\x0cpayrequestid\x18\x05 \x02(\t\"4\n\x06Result\x12*\n\nbaseresult\x18\x01 \x02(\x0b\x32\x16.BaseResult.BaseResultB \n\x11\x63om.nearme.pluginB\x0bSmsPbEntity')
  ,
  dependencies=[BaseResult_pb2.DESCRIPTOR,BaseHeader_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Sms.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Sms.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operate', full_name='Sms.Request.operate', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='verifycode', full_name='Sms.Request.verifycode', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='Sms.Request.sign', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payrequestid', full_name='Sms.Request.payrequestid', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=178,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Sms.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='Sms.Result.baseresult', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=232,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'SmsPb_pb2'
  # @@protoc_insertion_point(class_scope:Sms.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'SmsPb_pb2'
  # @@protoc_insertion_point(class_scope:Sms.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\013SmsPbEntity'))
# @@protoc_insertion_point(module_scope)
