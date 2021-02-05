# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: RechargeAndSpend.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from pb_src.python_standard import BaseHeaderOut_pb2
from pb_src.python_standard import Product_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='RechargeAndSpend.proto',
  package='',
  serialized_pb=_b('\n\x16RechargeAndSpend.proto\x1a\x13\x42\x61seHeaderOut.proto\x1a\rProduct.proto\"\xca\x04\n\x17RechargeAndSpendRequest\x12\x1e\n\x06header\x18\x01 \x02(\x0b\x32\x0e.BaseHeaderOut\x12\x14\n\x0cpartnerOrder\x18\x02 \x02(\t\x12\x11\n\tpartnerId\x18\x03 \x02(\t\x12\x0f\n\x07\x63ountry\x18\x04 \x02(\t\x12\x0f\n\x07payType\x18\x05 \x02(\t\x12\x0f\n\x07\x63hannel\x18\x06 \x02(\t\x12\x11\n\tpayAmount\x18\x07 \x02(\t\x12\x10\n\x08\x63urrency\x18\x08 \x02(\t\x12\x1c\n\x14\x63ocoinRechargeAmount\x18\t \x01(\t\x12\x17\n\x0f\x63ocoinPayAmount\x18\n \x01(\t\x12\x19\n\x07product\x18\x0b \x02(\x0b\x32\x08.Product\x12\x11\n\treturnUrl\x18\x0c \x01(\t\x12\x11\n\tnotifyUrl\x18\r \x01(\t\x12\x15\n\rpartnerParams\x18\x0e \x01(\t\x12\x14\n\x0c\x62usinessType\x18\x10 \x01(\t\x12\x19\n\x11\x62usinessChannelId\x18\x11 \x01(\t\x12\x10\n\x08\x63ouponId\x18\x15 \x01(\t\x12\x16\n\x0e\x64iscountAmount\x18\x16 \x01(\t\x12\x1b\n\x13\x62\x61nkCardAgreementNo\x18\x17 \x01(\t\x12\x19\n\x11hasAdditionalFees\x18\x1b \x01(\x08\x12\x0e\n\x06\x66\x61\x63tor\x18\x1c \x01(\t\x12\x15\n\rpayActivityId\x18\x1d \x01(\t\x12\x18\n\x10\x61\x64\x64itionalAmount\x18\x1e \x01(\t\x12\x16\n\x0e\x61\x63tivityAmount\x18\" \x01(\t\x12\x13\n\x0bphoneNumber\x18# \x01(\t\"\x94\x02\n\x18RechargeAndSpendResponse\x12\x11\n\tisSuccess\x18\x01 \x02(\x08\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\x44\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x36.RechargeAndSpendResponse.RechargeAndSpendResponseData\x1a\x83\x01\n\x1cRechargeAndSpendResponseData\x12\x14\n\x0cpayRequestId\x18\x01 \x02(\t\x12\x0e\n\x06payUrl\x18\x02 \x02(\t\x12\x12\n\nparameters\x18\x03 \x01(\t\x12\x18\n\x10\x63hannelReturnUrl\x18\x04 \x01(\t\x12\x0f\n\x07otpTime\x18\x05 \x01(\x03\x42\x13\n\x11\x63om.oppo.pay.bean')
  ,
  dependencies=[BaseHeaderOut_pb2.DESCRIPTOR,Product_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_RECHARGEANDSPENDREQUEST = _descriptor.Descriptor(
  name='RechargeAndSpendRequest',
  full_name='RechargeAndSpendRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='RechargeAndSpendRequest.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerOrder', full_name='RechargeAndSpendRequest.partnerOrder', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerId', full_name='RechargeAndSpendRequest.partnerId', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='RechargeAndSpendRequest.country', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payType', full_name='RechargeAndSpendRequest.payType', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channel', full_name='RechargeAndSpendRequest.channel', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payAmount', full_name='RechargeAndSpendRequest.payAmount', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currency', full_name='RechargeAndSpendRequest.currency', index=7,
      number=8, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cocoinRechargeAmount', full_name='RechargeAndSpendRequest.cocoinRechargeAmount', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cocoinPayAmount', full_name='RechargeAndSpendRequest.cocoinPayAmount', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='product', full_name='RechargeAndSpendRequest.product', index=10,
      number=11, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='returnUrl', full_name='RechargeAndSpendRequest.returnUrl', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='notifyUrl', full_name='RechargeAndSpendRequest.notifyUrl', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerParams', full_name='RechargeAndSpendRequest.partnerParams', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='businessType', full_name='RechargeAndSpendRequest.businessType', index=14,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='businessChannelId', full_name='RechargeAndSpendRequest.businessChannelId', index=15,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='couponId', full_name='RechargeAndSpendRequest.couponId', index=16,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='discountAmount', full_name='RechargeAndSpendRequest.discountAmount', index=17,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bankCardAgreementNo', full_name='RechargeAndSpendRequest.bankCardAgreementNo', index=18,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hasAdditionalFees', full_name='RechargeAndSpendRequest.hasAdditionalFees', index=19,
      number=27, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='factor', full_name='RechargeAndSpendRequest.factor', index=20,
      number=28, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payActivityId', full_name='RechargeAndSpendRequest.payActivityId', index=21,
      number=29, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='additionalAmount', full_name='RechargeAndSpendRequest.additionalAmount', index=22,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='activityAmount', full_name='RechargeAndSpendRequest.activityAmount', index=23,
      number=34, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='phoneNumber', full_name='RechargeAndSpendRequest.phoneNumber', index=24,
      number=35, type=9, cpp_type=9, label=1,
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
  serialized_start=63,
  serialized_end=649,
)


_RECHARGEANDSPENDRESPONSE_RECHARGEANDSPENDRESPONSEDATA = _descriptor.Descriptor(
  name='RechargeAndSpendResponseData',
  full_name='RechargeAndSpendResponse.RechargeAndSpendResponseData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payRequestId', full_name='RechargeAndSpendResponse.RechargeAndSpendResponseData.payRequestId', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payUrl', full_name='RechargeAndSpendResponse.RechargeAndSpendResponseData.payUrl', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='RechargeAndSpendResponse.RechargeAndSpendResponseData.parameters', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channelReturnUrl', full_name='RechargeAndSpendResponse.RechargeAndSpendResponseData.channelReturnUrl', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='otpTime', full_name='RechargeAndSpendResponse.RechargeAndSpendResponseData.otpTime', index=4,
      number=5, type=3, cpp_type=2, label=1,
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
  serialized_start=797,
  serialized_end=928,
)

_RECHARGEANDSPENDRESPONSE = _descriptor.Descriptor(
  name='RechargeAndSpendResponse',
  full_name='RechargeAndSpendResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isSuccess', full_name='RechargeAndSpendResponse.isSuccess', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='RechargeAndSpendResponse.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='RechargeAndSpendResponse.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='RechargeAndSpendResponse.data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RECHARGEANDSPENDRESPONSE_RECHARGEANDSPENDRESPONSEDATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=652,
  serialized_end=928,
)

_RECHARGEANDSPENDREQUEST.fields_by_name['header'].message_type = BaseHeaderOut_pb2._BASEHEADEROUT
_RECHARGEANDSPENDREQUEST.fields_by_name['product'].message_type = Product_pb2._PRODUCT
_RECHARGEANDSPENDRESPONSE_RECHARGEANDSPENDRESPONSEDATA.containing_type = _RECHARGEANDSPENDRESPONSE
_RECHARGEANDSPENDRESPONSE.fields_by_name['data'].message_type = _RECHARGEANDSPENDRESPONSE_RECHARGEANDSPENDRESPONSEDATA
DESCRIPTOR.message_types_by_name['RechargeAndSpendRequest'] = _RECHARGEANDSPENDREQUEST
DESCRIPTOR.message_types_by_name['RechargeAndSpendResponse'] = _RECHARGEANDSPENDRESPONSE

RechargeAndSpendRequest = _reflection.GeneratedProtocolMessageType('RechargeAndSpendRequest', (_message.Message,), dict(
  DESCRIPTOR = _RECHARGEANDSPENDREQUEST,
  __module__ = 'RechargeAndSpend_pb2'
  # @@protoc_insertion_point(class_scope:RechargeAndSpendRequest)
  ))
_sym_db.RegisterMessage(RechargeAndSpendRequest)

RechargeAndSpendResponse = _reflection.GeneratedProtocolMessageType('RechargeAndSpendResponse', (_message.Message,), dict(

  RechargeAndSpendResponseData = _reflection.GeneratedProtocolMessageType('RechargeAndSpendResponseData', (_message.Message,), dict(
    DESCRIPTOR = _RECHARGEANDSPENDRESPONSE_RECHARGEANDSPENDRESPONSEDATA,
    __module__ = 'RechargeAndSpend_pb2'
    # @@protoc_insertion_point(class_scope:RechargeAndSpendResponse.RechargeAndSpendResponseData)
    ))
  ,
  DESCRIPTOR = _RECHARGEANDSPENDRESPONSE,
  __module__ = 'RechargeAndSpend_pb2'
  # @@protoc_insertion_point(class_scope:RechargeAndSpendResponse)
  ))
_sym_db.RegisterMessage(RechargeAndSpendResponse)
_sym_db.RegisterMessage(RechargeAndSpendResponse.RechargeAndSpendResponseData)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.oppo.pay.bean'))
# @@protoc_insertion_point(module_scope)
