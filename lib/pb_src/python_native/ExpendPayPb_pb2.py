# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ExpendPayPb.proto

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
  name='ExpendPayPb.proto',
  package='ExpendPay',
  serialized_pb=_b('\n\x11\x45xpendPayPb.proto\x12\tExpendPay\x1a\x10\x42\x61seResult.proto\x1a\x10\x42\x61seHeader.proto\"\xb9\x03\n\x07request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\r\n\x05price\x18\x02 \x02(\x05\x12\r\n\x05\x63ount\x18\x03 \x02(\x05\x12\x13\n\x0bproductname\x18\x04 \x02(\t\x12\x13\n\x0bproductdesc\x18\x05 \x01(\t\x12\x11\n\tpartnerid\x18\x06 \x01(\t\x12\x13\n\x0b\x63\x61llBackUrl\x18\x07 \x02(\t\x12\x14\n\x0cpartnerOrder\x18\x08 \x02(\t\x12\x11\n\tchannelId\x18\t \x01(\t\x12\x0b\n\x03ver\x18\n \x01(\t\x12\x0e\n\x06source\x18\x0b \x01(\t\x12\x0e\n\x06\x61ttach\x18\x0c \x01(\t\x12\x0c\n\x04sign\x18\r \x02(\t\x12\x0f\n\x07paytype\x18\x0e \x01(\t\x12\x0e\n\x06\x61ppKey\x18\x0f \x01(\t\x12\x11\n\tvoucherId\x18\x10 \x01(\x05\x12\x13\n\x0bvoucherType\x18\x11 \x01(\x05\x12\x14\n\x0cvoucherCount\x18\x12 \x01(\x05\x12\r\n\x05order\x18\x13 \x01(\t\x12\n\n\x02ip\x18\x14 \x01(\t\x12\x0e\n\x06\x66\x61\x63tor\x18\x15 \x01(\t\x12\x12\n\nscreenInfo\x18\x16 \x01(\t\x12\x14\n\x0cuseVirCoupon\x18\x17 \x01(\t\"\x93\x01\n\x06Result\x12*\n\nbaseresult\x18\x01 \x02(\x0b\x32\x16.BaseResult.BaseResult\x12\x0c\n\x04rpay\x18\x02 \x01(\t\x12\x0c\n\x04gpay\x18\x03 \x01(\t\x12\x12\n\npayVouDesc\x18\x04 \x01(\t\x12\x16\n\x0evouCountDetail\x18\x05 \x01(\t\x12\x15\n\rnotClearCount\x18\x06 \x01(\x05\x42&\n\x11\x63om.nearme.pluginB\x11\x45xpendPayPbEntity')
  ,
  dependencies=[BaseResult_pb2.DESCRIPTOR,BaseHeader_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='request',
  full_name='ExpendPay.request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='ExpendPay.request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='price', full_name='ExpendPay.request.price', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='count', full_name='ExpendPay.request.count', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='productname', full_name='ExpendPay.request.productname', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='productdesc', full_name='ExpendPay.request.productdesc', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerid', full_name='ExpendPay.request.partnerid', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='callBackUrl', full_name='ExpendPay.request.callBackUrl', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerOrder', full_name='ExpendPay.request.partnerOrder', index=7,
      number=8, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channelId', full_name='ExpendPay.request.channelId', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ver', full_name='ExpendPay.request.ver', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='source', full_name='ExpendPay.request.source', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='attach', full_name='ExpendPay.request.attach', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='ExpendPay.request.sign', index=12,
      number=13, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='paytype', full_name='ExpendPay.request.paytype', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='appKey', full_name='ExpendPay.request.appKey', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voucherId', full_name='ExpendPay.request.voucherId', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voucherType', full_name='ExpendPay.request.voucherType', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voucherCount', full_name='ExpendPay.request.voucherCount', index=17,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='order', full_name='ExpendPay.request.order', index=18,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='ExpendPay.request.ip', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='factor', full_name='ExpendPay.request.factor', index=20,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='screenInfo', full_name='ExpendPay.request.screenInfo', index=21,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='useVirCoupon', full_name='ExpendPay.request.useVirCoupon', index=22,
      number=23, type=9, cpp_type=9, label=1,
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
  serialized_start=69,
  serialized_end=510,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='ExpendPay.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='ExpendPay.Result.baseresult', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rpay', full_name='ExpendPay.Result.rpay', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gpay', full_name='ExpendPay.Result.gpay', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payVouDesc', full_name='ExpendPay.Result.payVouDesc', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vouCountDetail', full_name='ExpendPay.Result.vouCountDetail', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='notClearCount', full_name='ExpendPay.Result.notClearCount', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=513,
  serialized_end=660,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
DESCRIPTOR.message_types_by_name['request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

request = _reflection.GeneratedProtocolMessageType('request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'ExpendPayPb_pb2'
  # @@protoc_insertion_point(class_scope:ExpendPay.request)
  ))
_sym_db.RegisterMessage(request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'ExpendPayPb_pb2'
  # @@protoc_insertion_point(class_scope:ExpendPay.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\021ExpendPayPbEntity'))
# @@protoc_insertion_point(module_scope)
