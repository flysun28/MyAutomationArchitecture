# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Balance.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import BaseHeaderOut_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Balance.proto',
  package='',
  serialized_pb=_b('\n\rBalance.proto\x1a\x13\x42\x61seHeaderOut.proto\"A\n\x0e\x42\x61lanceRequest\x12\x1e\n\x06header\x18\x01 \x02(\x0b\x32\x0e.BaseHeaderOut\x12\x0f\n\x07\x63ountry\x18\x02 \x02(\t\"\xe5\x01\n\rBalanceResult\x12\x11\n\tisSuccess\x18\x01 \x02(\x08\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12+\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x1d.BalanceResult.AuthResultData\x1ay\n\x0e\x41uthResultData\x12\x38\n\x08userInfo\x18\x03 \x02(\x0b\x32&.BalanceResult.AuthResultData.UserInfo\x1a-\n\x08UserInfo\x12\x0f\n\x07\x62\x61lance\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\tB\x13\n\x11\x63om.oppo.pay.bean')
  ,
  dependencies=[BaseHeaderOut_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BALANCEREQUEST = _descriptor.Descriptor(
  name='BalanceRequest',
  full_name='BalanceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='BalanceRequest.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='BalanceRequest.country', index=1,
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
  serialized_start=38,
  serialized_end=103,
)


_BALANCERESULT_AUTHRESULTDATA_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='BalanceResult.AuthResultData.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='balance', full_name='BalanceResult.AuthResultData.UserInfo.balance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username', full_name='BalanceResult.AuthResultData.UserInfo.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=290,
  serialized_end=335,
)

_BALANCERESULT_AUTHRESULTDATA = _descriptor.Descriptor(
  name='AuthResultData',
  full_name='BalanceResult.AuthResultData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='userInfo', full_name='BalanceResult.AuthResultData.userInfo', index=0,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_BALANCERESULT_AUTHRESULTDATA_USERINFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=335,
)

_BALANCERESULT = _descriptor.Descriptor(
  name='BalanceResult',
  full_name='BalanceResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isSuccess', full_name='BalanceResult.isSuccess', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='BalanceResult.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='BalanceResult.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='BalanceResult.data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_BALANCERESULT_AUTHRESULTDATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=335,
)

_BALANCEREQUEST.fields_by_name['header'].message_type = BaseHeaderOut_pb2._BASEHEADEROUT
_BALANCERESULT_AUTHRESULTDATA_USERINFO.containing_type = _BALANCERESULT_AUTHRESULTDATA
_BALANCERESULT_AUTHRESULTDATA.fields_by_name['userInfo'].message_type = _BALANCERESULT_AUTHRESULTDATA_USERINFO
_BALANCERESULT_AUTHRESULTDATA.containing_type = _BALANCERESULT
_BALANCERESULT.fields_by_name['data'].message_type = _BALANCERESULT_AUTHRESULTDATA
DESCRIPTOR.message_types_by_name['BalanceRequest'] = _BALANCEREQUEST
DESCRIPTOR.message_types_by_name['BalanceResult'] = _BALANCERESULT

BalanceRequest = _reflection.GeneratedProtocolMessageType('BalanceRequest', (_message.Message,), dict(
  DESCRIPTOR = _BALANCEREQUEST,
  __module__ = 'Balance_pb2'
  # @@protoc_insertion_point(class_scope:BalanceRequest)
  ))
_sym_db.RegisterMessage(BalanceRequest)

BalanceResult = _reflection.GeneratedProtocolMessageType('BalanceResult', (_message.Message,), dict(

  AuthResultData = _reflection.GeneratedProtocolMessageType('AuthResultData', (_message.Message,), dict(

    UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), dict(
      DESCRIPTOR = _BALANCERESULT_AUTHRESULTDATA_USERINFO,
      __module__ = 'Balance_pb2'
      # @@protoc_insertion_point(class_scope:BalanceResult.AuthResultData.UserInfo)
      ))
    ,
    DESCRIPTOR = _BALANCERESULT_AUTHRESULTDATA,
    __module__ = 'Balance_pb2'
    # @@protoc_insertion_point(class_scope:BalanceResult.AuthResultData)
    ))
  ,
  DESCRIPTOR = _BALANCERESULT,
  __module__ = 'Balance_pb2'
  # @@protoc_insertion_point(class_scope:BalanceResult)
  ))
_sym_db.RegisterMessage(BalanceResult)
_sym_db.RegisterMessage(BalanceResult.AuthResultData)
_sym_db.RegisterMessage(BalanceResult.AuthResultData.UserInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.oppo.pay.bean'))
# @@protoc_insertion_point(module_scope)
