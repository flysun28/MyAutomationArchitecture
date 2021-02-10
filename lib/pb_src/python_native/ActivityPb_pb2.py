# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ActivityPb.proto

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
  name='ActivityPb.proto',
  package='Activity',
  serialized_pb=_b('\n\x10\x41\x63tivityPb.proto\x12\x08\x41\x63tivity\x1a\x10\x42\x61seResult.proto\x1a\x10\x42\x61seHeader.proto\"\x93\x01\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x0e\n\x06\x61mount\x18\x02 \x01(\t\x12\x0f\n\x07paytype\x18\x03 \x01(\t\x12\x0c\n\x04\x65xt1\x18\x04 \x01(\t\x12\x0c\n\x04\x65xt2\x18\x05 \x01(\t\x12\x0e\n\x06remark\x18\x06 \x01(\t\x12\x13\n\x0bpaymentType\x18\x07 \x01(\t\"\xb7\x01\n\x06Result\x12*\n\nbaseresult\x18\x01 \x02(\x0b\x32\x16.BaseResult.BaseResult\x12\x11\n\tpayAmount\x18\x02 \x01(\t\x12\x13\n\x0borigiAmount\x18\x03 \x01(\t\x12,\n\x0c\x41\x63tivityItem\x18\x04 \x03(\x0b\x32\x16.Activity.ActivityItem\x12\x0f\n\x07paytype\x18\x05 \x01(\t\x12\x0c\n\x04\x65xt1\x18\x06 \x01(\t\x12\x0c\n\x04\x65xt2\x18\x07 \x01(\t\":\n\x0c\x41\x63tivityItem\x12\x15\n\rpresentAmount\x18\x01 \x02(\t\x12\x13\n\x0bpresentName\x18\x02 \x02(\tB%\n\x11\x63om.nearme.pluginB\x10\x41\x63tivityPbEntity')
  ,
  dependencies=[BaseResult_pb2.DESCRIPTOR,BaseHeader_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Activity.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Activity.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='Activity.Request.amount', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='paytype', full_name='Activity.Request.paytype', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext1', full_name='Activity.Request.ext1', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext2', full_name='Activity.Request.ext2', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='remark', full_name='Activity.Request.remark', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='paymentType', full_name='Activity.Request.paymentType', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=67,
  serialized_end=214,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Activity.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='Activity.Result.baseresult', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payAmount', full_name='Activity.Result.payAmount', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='origiAmount', full_name='Activity.Result.origiAmount', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ActivityItem', full_name='Activity.Result.ActivityItem', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='paytype', full_name='Activity.Result.paytype', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext1', full_name='Activity.Result.ext1', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext2', full_name='Activity.Result.ext2', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=217,
  serialized_end=400,
)


_ACTIVITYITEM = _descriptor.Descriptor(
  name='ActivityItem',
  full_name='Activity.ActivityItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='presentAmount', full_name='Activity.ActivityItem.presentAmount', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='presentName', full_name='Activity.ActivityItem.presentName', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=402,
  serialized_end=460,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
_RESULT.fields_by_name['ActivityItem'].message_type = _ACTIVITYITEM
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['ActivityItem'] = _ACTIVITYITEM

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'ActivityPb_pb2'
  # @@protoc_insertion_point(class_scope:Activity.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'ActivityPb_pb2'
  # @@protoc_insertion_point(class_scope:Activity.Result)
  ))
_sym_db.RegisterMessage(Result)

ActivityItem = _reflection.GeneratedProtocolMessageType('ActivityItem', (_message.Message,), dict(
  DESCRIPTOR = _ACTIVITYITEM,
  __module__ = 'ActivityPb_pb2'
  # @@protoc_insertion_point(class_scope:Activity.ActivityItem)
  ))
_sym_db.RegisterMessage(ActivityItem)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\020ActivityPbEntity'))
# @@protoc_insertion_point(module_scope)
