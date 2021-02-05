# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AutoRenewPb.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from pb_src.python_native import BaseResult_pb2
from pb_src.python_native import BaseHeader_pb2
from pb_src.python_native import BasePayPb_pb2
from pb_src.python_native import ExpendPayPb_pb2

DESCRIPTOR = _descriptor.FileDescriptor(
  name='AutoRenewPb.proto',
  package='AutoRenew',
  serialized_pb=_b('\n\x11\x41utoRenewPb.proto\x12\tAutoRenew\x1a\x10\x42\x61seResult.proto\x1a\x10\x42\x61seHeader.proto\x1a\x0f\x42\x61sePayPb.proto\x1a\x11\x45xpendPayPb.proto\"\xf9\x03\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x11\n\ttransType\x18\x02 \x02(\t\x12\x18\n\x10renewProductCode\x18\x03 \x01(\t\x12\x18\n\x10signPartnerOrder\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x02(\t\x12\x13\n\x0bthirdPartId\x18\x06 \x01(\t\x12\x0e\n\x06\x61mount\x18\x07 \x02(\t\x12\x11\n\toriAmount\x18\x08 \x01(\t\x12\x0e\n\x06mobile\x18\t \x01(\t\x12\n\n\x02ip\x18\n \x01(\t\x12\x0c\n\x04sign\x18\x0b \x01(\t\x12\x14\n\x0cpartnerPrice\x18\x0c \x01(\t\x12\x14\n\x0cpartnerCount\x18\r \x01(\t\x12\x14\n\x0creturnAppUrl\x18\x0e \x01(\t\x12\x1e\n\x16signAgreementNotifyUrl\x18\x0f \x01(\t\x12\r\n\x05\x61ppId\x18\x10 \x01(\t\x12\x13\n\x0bpartnerSign\x18\x11 \x01(\t\x12\x14\n\x0cisNeedExpend\x18\x12 \x01(\t\x12!\n\x07\x62\x61sepay\x18\x13 \x02(\x0b\x32\x10.BasePay.BasePay\x12)\n\rexpendRequest\x18\x14 \x01(\x0b\x32\x12.ExpendPay.request\x12\x12\n\nscreenInfo\x18\x15 \x01(\t\x12\x11\n\textraInfo\x18\x16 \x01(\t\"o\n\x06Result\x12*\n\nbaseresult\x18\x01 \x02(\x0b\x32\x16.BaseResult.BaseResult\x12\x14\n\x0cpayrequestid\x18\x04 \x02(\t\x12\x11\n\ttransType\x18\x05 \x01(\t\x12\x10\n\x08signType\x18\x06 \x01(\tB&\n\x11\x63om.nearme.pluginB\x11\x41utoRenewPbEntity')
  ,
  dependencies=[BaseResult_pb2.DESCRIPTOR,BaseHeader_pb2.DESCRIPTOR,BasePayPb_pb2.DESCRIPTOR,ExpendPayPb_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='AutoRenew.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='AutoRenew.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transType', full_name='AutoRenew.Request.transType', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='renewProductCode', full_name='AutoRenew.Request.renewProductCode', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signPartnerOrder', full_name='AutoRenew.Request.signPartnerOrder', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='AutoRenew.Request.type', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='thirdPartId', full_name='AutoRenew.Request.thirdPartId', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='AutoRenew.Request.amount', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oriAmount', full_name='AutoRenew.Request.oriAmount', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mobile', full_name='AutoRenew.Request.mobile', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='AutoRenew.Request.ip', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='AutoRenew.Request.sign', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerPrice', full_name='AutoRenew.Request.partnerPrice', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerCount', full_name='AutoRenew.Request.partnerCount', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='returnAppUrl', full_name='AutoRenew.Request.returnAppUrl', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signAgreementNotifyUrl', full_name='AutoRenew.Request.signAgreementNotifyUrl', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='appId', full_name='AutoRenew.Request.appId', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerSign', full_name='AutoRenew.Request.partnerSign', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isNeedExpend', full_name='AutoRenew.Request.isNeedExpend', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='basepay', full_name='AutoRenew.Request.basepay', index=18,
      number=19, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expendRequest', full_name='AutoRenew.Request.expendRequest', index=19,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='screenInfo', full_name='AutoRenew.Request.screenInfo', index=20,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='extraInfo', full_name='AutoRenew.Request.extraInfo', index=21,
      number=22, type=9, cpp_type=9, label=1,
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
  serialized_start=105,
  serialized_end=610,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='AutoRenew.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='AutoRenew.Result.baseresult', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payrequestid', full_name='AutoRenew.Result.payrequestid', index=1,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transType', full_name='AutoRenew.Result.transType', index=2,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signType', full_name='AutoRenew.Result.signType', index=3,
      number=6, type=9, cpp_type=9, label=1,
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
  serialized_start=612,
  serialized_end=723,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_REQUEST.fields_by_name['basepay'].message_type = BasePayPb_pb2._BASEPAY
_REQUEST.fields_by_name['expendRequest'].message_type = ExpendPayPb_pb2._REQUEST
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'AutoRenewPb_pb2'
  # @@protoc_insertion_point(class_scope:AutoRenew.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'AutoRenewPb_pb2'
  # @@protoc_insertion_point(class_scope:AutoRenew.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\021AutoRenewPbEntity'))
# @@protoc_insertion_point(module_scope)
