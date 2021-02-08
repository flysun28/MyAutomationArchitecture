# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: BindCardInfoPb.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import BaseResult_pb2
from . import BaseHeader_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='BindCardInfoPb.proto',
  package='BindCardInfo',
  serialized_pb=_b('\n\x14\x42indCardInfoPb.proto\x12\x0c\x42indCardInfo\x1a\x10\x42\x61seResult.proto\x1a\x10\x42\x61seHeader.proto\"P\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x0f\n\x07paytype\x18\x02 \x01(\t\x12\x0c\n\x04sign\x18\x03 \x02(\t\"f\n\x06Result\x12*\n\nbaseresult\x18\x01 \x02(\x0b\x32\x16.BaseResult.BaseResult\x12\x30\n\x0c\x62indinfoitem\x18\x02 \x03(\x0b\x32\x1a.BindCardInfo.BindinfoItem\"\x9f\x01\n\x0c\x42indinfoItem\x12\x12\n\npaychannel\x18\x01 \x01(\t\x12\x10\n\x08\x62\x61nkname\x18\x02 \x01(\t\x12\x13\n\x0b\x65ncrycardno\x18\x03 \x01(\t\x12\x0b\n\x03\x65xt\x18\x04 \x01(\t\x12\x0c\n\x04icon\x18\x05 \x01(\t\x12\x11\n\tmaxamount\x18\x06 \x01(\t\x12\x12\n\nlimitToday\x18\x07 \x01(\t\x12\x12\n\nlimitMonth\x18\x08 \x01(\tB)\n\x11\x63om.nearme.pluginB\x14\x42indCardInfoPbEntity')
  ,
  dependencies=[BaseResult_pb2.DESCRIPTOR,BaseHeader_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='BindCardInfo.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='BindCardInfo.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='paytype', full_name='BindCardInfo.Request.paytype', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='BindCardInfo.Request.sign', index=2,
      number=3, type=9, cpp_type=9, label=2,
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
  serialized_start=74,
  serialized_end=154,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='BindCardInfo.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='BindCardInfo.Result.baseresult', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bindinfoitem', full_name='BindCardInfo.Result.bindinfoitem', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=156,
  serialized_end=258,
)


_BINDINFOITEM = _descriptor.Descriptor(
  name='BindinfoItem',
  full_name='BindCardInfo.BindinfoItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='paychannel', full_name='BindCardInfo.BindinfoItem.paychannel', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bankname', full_name='BindCardInfo.BindinfoItem.bankname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='encrycardno', full_name='BindCardInfo.BindinfoItem.encrycardno', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext', full_name='BindCardInfo.BindinfoItem.ext', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='icon', full_name='BindCardInfo.BindinfoItem.icon', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maxamount', full_name='BindCardInfo.BindinfoItem.maxamount', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='limitToday', full_name='BindCardInfo.BindinfoItem.limitToday', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='limitMonth', full_name='BindCardInfo.BindinfoItem.limitMonth', index=7,
      number=8, type=9, cpp_type=9, label=1,
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
  serialized_start=261,
  serialized_end=420,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
_RESULT.fields_by_name['bindinfoitem'].message_type = _BINDINFOITEM
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['BindinfoItem'] = _BINDINFOITEM

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'BindCardInfoPb_pb2'
  # @@protoc_insertion_point(class_scope:BindCardInfo.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'BindCardInfoPb_pb2'
  # @@protoc_insertion_point(class_scope:BindCardInfo.Result)
  ))
_sym_db.RegisterMessage(Result)

BindinfoItem = _reflection.GeneratedProtocolMessageType('BindinfoItem', (_message.Message,), dict(
  DESCRIPTOR = _BINDINFOITEM,
  __module__ = 'BindCardInfoPb_pb2'
  # @@protoc_insertion_point(class_scope:BindCardInfo.BindinfoItem)
  ))
_sym_db.RegisterMessage(BindinfoItem)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\024BindCardInfoPbEntity'))
# @@protoc_insertion_point(module_scope)
