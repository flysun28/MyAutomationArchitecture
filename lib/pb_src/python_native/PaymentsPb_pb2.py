# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PaymentsPb.proto

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
  name='PaymentsPb.proto',
  package='Payments',
  serialized_pb=_b('\n\x10PaymentsPb.proto\x12\x08Payments\x1a\x10\x42\x61seHeader.proto\x1a\x10\x42\x61seResult.proto\"\xb4\x03\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x0c\n\x04sign\x18\x02 \x02(\t\x12\x14\n\x0cvalueversion\x18\x03 \x01(\t\x12\x0e\n\x06\x61mount\x18\x04 \x01(\t\x12\x13\n\x0bpartnercode\x18\x05 \x01(\t\x12\x12\n\nsimoneimsi\x18\x06 \x01(\t\x12\x12\n\nsimtwoimsi\x18\x07 \x01(\t\x12\x11\n\tchannelId\x18\x08 \x01(\t\x12\n\n\x02ip\x18\t \x01(\t\x12\x0f\n\x07renewal\x18\n \x01(\t\x12\x15\n\rwalletVersion\x18\x0b \x01(\t\x12\x15\n\roppoucVersion\x18\x0c \x01(\t\x12\x17\n\x0f\x61utoRenewalSign\x18\r \x01(\t\x12\r\n\x05\x61ppId\x18\x0e \x01(\t\x12\x12\n\nappVersion\x18\x0f \x01(\t\x12\x11\n\tucVersion\x18\x10 \x01(\t\x12\x18\n\x10renewProductCode\x18\x11 \x01(\t\x12\x11\n\tisAccount\x18\x12 \x01(\t\x12\x12\n\nbuyPlaceId\x18\x13 \x01(\t\x12\x12\n\npartnerVip\x18\x14 \x01(\t\x12\x0e\n\x06\x66\x61\x63tor\x18\x15 \x01(\t\"\xad\x02\n\x06Result\x12\x15\n\rpaytypestatus\x18\x01 \x02(\t\x12-\n\x0b\x63hannelItem\x18\x02 \x03(\x0b\x32\x18.Payments.PaychannelItem\x12\x14\n\x0cvalueversion\x18\x03 \x02(\t\x12*\n\nbaseresult\x18\x04 \x01(\x0b\x32\x16.BaseResult.BaseResult\x12\x13\n\x0bselectedSim\x18\x05 \x01(\t\x12\x0f\n\x07isLogin\x18\x06 \x01(\x08\x12\x0b\n\x03t_p\x18\x07 \x01(\t\x12\x0b\n\x03s_p\x18\x08 \x01(\t\x12\x0b\n\x03m_p\x18\t \x01(\t\x12$\n\x08\x62uyPlace\x18\n \x01(\x0b\x32\x12.Payments.BuyPlace\x12(\n\npartnerVip\x18\x0b \x01(\x0b\x32\x14.Payments.PartnerVip\"\xde\x03\n\x0ePaychannelItem\x12\x0f\n\x07\x63hannel\x18\x01 \x02(\t\x12\x13\n\x0bpaytypename\x18\x02 \x02(\t\x12\x0c\n\x04icon\x18\x03 \x02(\t\x12\x0e\n\x06prompt\x18\x04 \x02(\t\x12\x11\n\tmaxamount\x18\x05 \x02(\t\x12\x10\n\x08showtype\x18\x06 \x02(\t\x12\x13\n\x0blastpaytype\x18\x07 \x02(\t\x12\x0f\n\x07orderno\x18\x08 \x02(\t\x12\x12\n\nshowstatus\x18\t \x02(\t\x12\x0b\n\x03\x65xt\x18\n \x01(\t\x12\x11\n\tfrontname\x18\x0b \x01(\t\x12\x17\n\x0finControlOfRisk\x18\x0c \x01(\t\x12\r\n\x05limit\x18\r \x01(\t\x12\x12\n\nlimitToday\x18\x0e \x01(\t\x12\x12\n\nlimitMonth\x18\x0f \x01(\t\x12\x11\n\tsmallIcon\x18\x10 \x01(\t\x12\x15\n\rpromotionIcon\x18\x11 \x01(\t\x12\x17\n\x0fpromotionPrompt\x18\x12 \x01(\t\x12\x36\n\nsubscripts\x18\x13 \x03(\x0b\x32\".Payments.PaychannelItem.Subscript\x1a>\n\tSubscript\x12\x16\n\x0esubscriptsType\x18\x01 \x02(\t\x12\x19\n\x11subscriptsContent\x18\x02 \x02(\t\"\x89\x02\n\x08\x42uyPlace\x12\x14\n\x0c\x62uyPlaceType\x18\x01 \x01(\t\x12\x12\n\nbuyPlaceId\x18\x02 \x01(\t\x12\x15\n\rbuyPlaceTitle\x18\x03 \x01(\t\x12\x14\n\x0c\x62uyPlaceDesc\x18\x04 \x01(\t\x12\x15\n\rdiscountCount\x18\x05 \x01(\t\x12\x16\n\x0e\x64iscountAmount\x18\x06 \x01(\t\x12\x14\n\x0c\x64iscountType\x18\x07 \x01(\t\x12\x15\n\rdiscountVirId\x18\x08 \x01(\t\x12\x19\n\x11\x61ttachGoodsAmount\x18\t \x01(\t\x12\x1b\n\x13\x61ttachGoodsDiscount\x18\n \x01(\t\x12\x12\n\npartnerVip\x18\x0b \x01(\t\"m\n\nPartnerVip\x12\x16\n\x0epartnerVipDesc\x18\x01 \x01(\t\x12\x16\n\x0epartnerVipName\x18\x02 \x01(\t\x12\x15\n\rpartnerVipUrl\x18\x03 \x01(\t\x12\x18\n\x10partnerVipImgUrl\x18\x04 \x01(\tB%\n\x11\x63om.nearme.pluginB\x10PaymentsPbEntity')
  ,
  dependencies=[BaseHeader_pb2.DESCRIPTOR,BaseResult_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Payments.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Payments.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='Payments.Request.sign', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='valueversion', full_name='Payments.Request.valueversion', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='Payments.Request.amount', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnercode', full_name='Payments.Request.partnercode', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='simoneimsi', full_name='Payments.Request.simoneimsi', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='simtwoimsi', full_name='Payments.Request.simtwoimsi', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channelId', full_name='Payments.Request.channelId', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='Payments.Request.ip', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='renewal', full_name='Payments.Request.renewal', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='walletVersion', full_name='Payments.Request.walletVersion', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oppoucVersion', full_name='Payments.Request.oppoucVersion', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='autoRenewalSign', full_name='Payments.Request.autoRenewalSign', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='appId', full_name='Payments.Request.appId', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='appVersion', full_name='Payments.Request.appVersion', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ucVersion', full_name='Payments.Request.ucVersion', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='renewProductCode', full_name='Payments.Request.renewProductCode', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isAccount', full_name='Payments.Request.isAccount', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyPlaceId', full_name='Payments.Request.buyPlaceId', index=18,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerVip', full_name='Payments.Request.partnerVip', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='factor', full_name='Payments.Request.factor', index=20,
      number=21, type=9, cpp_type=9, label=1,
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
  serialized_end=503,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Payments.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='paytypestatus', full_name='Payments.Result.paytypestatus', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channelItem', full_name='Payments.Result.channelItem', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='valueversion', full_name='Payments.Result.valueversion', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='Payments.Result.baseresult', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='selectedSim', full_name='Payments.Result.selectedSim', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isLogin', full_name='Payments.Result.isLogin', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='t_p', full_name='Payments.Result.t_p', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='s_p', full_name='Payments.Result.s_p', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='m_p', full_name='Payments.Result.m_p', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyPlace', full_name='Payments.Result.buyPlace', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerVip', full_name='Payments.Result.partnerVip', index=10,
      number=11, type=11, cpp_type=10, label=1,
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
  serialized_start=506,
  serialized_end=807,
)


_PAYCHANNELITEM_SUBSCRIPT = _descriptor.Descriptor(
  name='Subscript',
  full_name='Payments.PaychannelItem.Subscript',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='subscriptsType', full_name='Payments.PaychannelItem.Subscript.subscriptsType', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subscriptsContent', full_name='Payments.PaychannelItem.Subscript.subscriptsContent', index=1,
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
  serialized_start=1226,
  serialized_end=1288,
)

_PAYCHANNELITEM = _descriptor.Descriptor(
  name='PaychannelItem',
  full_name='Payments.PaychannelItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='channel', full_name='Payments.PaychannelItem.channel', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='paytypename', full_name='Payments.PaychannelItem.paytypename', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='icon', full_name='Payments.PaychannelItem.icon', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='prompt', full_name='Payments.PaychannelItem.prompt', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maxamount', full_name='Payments.PaychannelItem.maxamount', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='showtype', full_name='Payments.PaychannelItem.showtype', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lastpaytype', full_name='Payments.PaychannelItem.lastpaytype', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='orderno', full_name='Payments.PaychannelItem.orderno', index=7,
      number=8, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='showstatus', full_name='Payments.PaychannelItem.showstatus', index=8,
      number=9, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext', full_name='Payments.PaychannelItem.ext', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frontname', full_name='Payments.PaychannelItem.frontname', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inControlOfRisk', full_name='Payments.PaychannelItem.inControlOfRisk', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='limit', full_name='Payments.PaychannelItem.limit', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='limitToday', full_name='Payments.PaychannelItem.limitToday', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='limitMonth', full_name='Payments.PaychannelItem.limitMonth', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='smallIcon', full_name='Payments.PaychannelItem.smallIcon', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='promotionIcon', full_name='Payments.PaychannelItem.promotionIcon', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='promotionPrompt', full_name='Payments.PaychannelItem.promotionPrompt', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subscripts', full_name='Payments.PaychannelItem.subscripts', index=18,
      number=19, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PAYCHANNELITEM_SUBSCRIPT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=810,
  serialized_end=1288,
)


_BUYPLACE = _descriptor.Descriptor(
  name='BuyPlace',
  full_name='Payments.BuyPlace',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buyPlaceType', full_name='Payments.BuyPlace.buyPlaceType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyPlaceId', full_name='Payments.BuyPlace.buyPlaceId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyPlaceTitle', full_name='Payments.BuyPlace.buyPlaceTitle', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyPlaceDesc', full_name='Payments.BuyPlace.buyPlaceDesc', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='discountCount', full_name='Payments.BuyPlace.discountCount', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='discountAmount', full_name='Payments.BuyPlace.discountAmount', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='discountType', full_name='Payments.BuyPlace.discountType', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='discountVirId', full_name='Payments.BuyPlace.discountVirId', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='attachGoodsAmount', full_name='Payments.BuyPlace.attachGoodsAmount', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='attachGoodsDiscount', full_name='Payments.BuyPlace.attachGoodsDiscount', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerVip', full_name='Payments.BuyPlace.partnerVip', index=10,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=1291,
  serialized_end=1556,
)


_PARTNERVIP = _descriptor.Descriptor(
  name='PartnerVip',
  full_name='Payments.PartnerVip',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partnerVipDesc', full_name='Payments.PartnerVip.partnerVipDesc', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerVipName', full_name='Payments.PartnerVip.partnerVipName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerVipUrl', full_name='Payments.PartnerVip.partnerVipUrl', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerVipImgUrl', full_name='Payments.PartnerVip.partnerVipImgUrl', index=3,
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
  serialized_start=1558,
  serialized_end=1667,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_RESULT.fields_by_name['channelItem'].message_type = _PAYCHANNELITEM
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
_RESULT.fields_by_name['buyPlace'].message_type = _BUYPLACE
_RESULT.fields_by_name['partnerVip'].message_type = _PARTNERVIP
_PAYCHANNELITEM_SUBSCRIPT.containing_type = _PAYCHANNELITEM
_PAYCHANNELITEM.fields_by_name['subscripts'].message_type = _PAYCHANNELITEM_SUBSCRIPT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['PaychannelItem'] = _PAYCHANNELITEM
DESCRIPTOR.message_types_by_name['BuyPlace'] = _BUYPLACE
DESCRIPTOR.message_types_by_name['PartnerVip'] = _PARTNERVIP

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'PaymentsPb_pb2'
  # @@protoc_insertion_point(class_scope:Payments.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'PaymentsPb_pb2'
  # @@protoc_insertion_point(class_scope:Payments.Result)
  ))
_sym_db.RegisterMessage(Result)

PaychannelItem = _reflection.GeneratedProtocolMessageType('PaychannelItem', (_message.Message,), dict(

  Subscript = _reflection.GeneratedProtocolMessageType('Subscript', (_message.Message,), dict(
    DESCRIPTOR = _PAYCHANNELITEM_SUBSCRIPT,
    __module__ = 'PaymentsPb_pb2'
    # @@protoc_insertion_point(class_scope:Payments.PaychannelItem.Subscript)
    ))
  ,
  DESCRIPTOR = _PAYCHANNELITEM,
  __module__ = 'PaymentsPb_pb2'
  # @@protoc_insertion_point(class_scope:Payments.PaychannelItem)
  ))
_sym_db.RegisterMessage(PaychannelItem)
_sym_db.RegisterMessage(PaychannelItem.Subscript)

BuyPlace = _reflection.GeneratedProtocolMessageType('BuyPlace', (_message.Message,), dict(
  DESCRIPTOR = _BUYPLACE,
  __module__ = 'PaymentsPb_pb2'
  # @@protoc_insertion_point(class_scope:Payments.BuyPlace)
  ))
_sym_db.RegisterMessage(BuyPlace)

PartnerVip = _reflection.GeneratedProtocolMessageType('PartnerVip', (_message.Message,), dict(
  DESCRIPTOR = _PARTNERVIP,
  __module__ = 'PaymentsPb_pb2'
  # @@protoc_insertion_point(class_scope:Payments.PartnerVip)
  ))
_sym_db.RegisterMessage(PartnerVip)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\020PaymentsPbEntity'))
# @@protoc_insertion_point(module_scope)
