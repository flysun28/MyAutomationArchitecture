# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: JudgebankPb.proto

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
  name='JudgebankPb.proto',
  package='Judgebank',
  serialized_pb=_b('\n\x11JudgebankPb.proto\x12\tJudgebank\x1a\x10\x42\x61seResult.proto\x1a\x10\x42\x61seHeader.proto\"a\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x10\n\x08\x63\x61rdtype\x18\x02 \x02(\t\x12\x0e\n\x06\x63\x61rdno\x18\x03 \x02(\t\x12\x0c\n\x04sign\x18\x04 \x02(\t\"j\n\x06Result\x12*\n\nbaseresult\x18\x01 \x02(\x0b\x32\x16.BaseResult.BaseResult\x12\x10\n\x08\x63\x61rdtype\x18\x02 \x01(\t\x12\x10\n\x08\x62\x61nkcode\x18\x03 \x01(\t\x12\x10\n\x08\x62\x61nkname\x18\x04 \x01(\tB&\n\x11\x63om.nearme.pluginB\x11JudgebankPbEntity')
  ,
  dependencies=[BaseResult_pb2.DESCRIPTOR,BaseHeader_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Judgebank.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Judgebank.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cardtype', full_name='Judgebank.Request.cardtype', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cardno', full_name='Judgebank.Request.cardno', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='Judgebank.Request.sign', index=3,
      number=4, type=9, cpp_type=9, label=2,
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
  serialized_start=68,
  serialized_end=165,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Judgebank.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='Judgebank.Result.baseresult', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cardtype', full_name='Judgebank.Result.cardtype', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bankcode', full_name='Judgebank.Result.bankcode', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bankname', full_name='Judgebank.Result.bankname', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=167,
  serialized_end=273,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'JudgebankPb_pb2'
  # @@protoc_insertion_point(class_scope:Judgebank.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'JudgebankPb_pb2'
  # @@protoc_insertion_point(class_scope:Judgebank.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\021JudgebankPbEntity'))
# @@protoc_insertion_point(module_scope)
