# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CocoinGearQuery.proto

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
from . import Exchange_pb2



DESCRIPTOR = _descriptor.FileDescriptor(
  name='CocoinGearQuery.proto',
  package='',
  serialized_pb=_b('\n\x15\x43ocoinGearQuery.proto\x1a\x13\x42\x61seHeaderOut.proto\x1a\x0e\x45xchange.proto\"i\n\x11\x43ocoinGearRequest\x12\x1e\n\x06header\x18\x01 \x02(\x0b\x32\x0e.BaseHeaderOut\x12\x0f\n\x07\x63ountry\x18\x02 \x02(\t\x12\x10\n\x08\x63urrency\x18\x03 \x02(\t\x12\x11\n\tpartnerId\x18\x04 \x02(\t\"\xed\x02\n\x10\x43ocoinGearResult\x12\x11\n\tisSuccess\x18\x01 \x02(\x08\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\x34\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32&.CocoinGearResult.CocoinGearResultData\x12>\n\x12\x65xchangeResultData\x18\x05 \x03(\x0b\x32\".ExchangeResult.ExchangeResultData\x12\x12\n\nactivityId\x18\x06 \x01(\t\x1aK\n\x0e\x43ocoinGearInfo\x12\x12\n\ncocoinGear\x18\x01 \x02(\t\x12\x15\n\rcocoinPresent\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\t\x1aT\n\x14\x43ocoinGearResultData\x12<\n\x12\x63ocoinGearInfoList\x18\x01 \x03(\x0b\x32 .CocoinGearResult.CocoinGearInfoB\x13\n\x11\x63om.oppo.pay.bean')
  ,
  dependencies=[BaseHeaderOut_pb2.DESCRIPTOR,Exchange_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_COCOINGEARREQUEST = _descriptor.Descriptor(
  name='CocoinGearRequest',
  full_name='CocoinGearRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='CocoinGearRequest.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='CocoinGearRequest.country', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currency', full_name='CocoinGearRequest.currency', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='partnerId', full_name='CocoinGearRequest.partnerId', index=3,
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
  serialized_start=62,
  serialized_end=167,
)


_COCOINGEARRESULT_COCOINGEARINFO = _descriptor.Descriptor(
  name='CocoinGearInfo',
  full_name='CocoinGearResult.CocoinGearInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cocoinGear', full_name='CocoinGearResult.CocoinGearInfo.cocoinGear', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cocoinPresent', full_name='CocoinGearResult.CocoinGearInfo.cocoinPresent', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='CocoinGearResult.CocoinGearInfo.amount', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=374,
  serialized_end=449,
)

_COCOINGEARRESULT_COCOINGEARRESULTDATA = _descriptor.Descriptor(
  name='CocoinGearResultData',
  full_name='CocoinGearResult.CocoinGearResultData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cocoinGearInfoList', full_name='CocoinGearResult.CocoinGearResultData.cocoinGearInfoList', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=451,
  serialized_end=535,
)

_COCOINGEARRESULT = _descriptor.Descriptor(
  name='CocoinGearResult',
  full_name='CocoinGearResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isSuccess', full_name='CocoinGearResult.isSuccess', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='CocoinGearResult.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='CocoinGearResult.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='CocoinGearResult.data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exchangeResultData', full_name='CocoinGearResult.exchangeResultData', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='activityId', full_name='CocoinGearResult.activityId', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_COCOINGEARRESULT_COCOINGEARINFO, _COCOINGEARRESULT_COCOINGEARRESULTDATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=170,
  serialized_end=535,
)

_COCOINGEARREQUEST.fields_by_name['header'].message_type = BaseHeaderOut_pb2._BASEHEADEROUT
_COCOINGEARRESULT_COCOINGEARINFO.containing_type = _COCOINGEARRESULT
_COCOINGEARRESULT_COCOINGEARRESULTDATA.fields_by_name['cocoinGearInfoList'].message_type = _COCOINGEARRESULT_COCOINGEARINFO
_COCOINGEARRESULT_COCOINGEARRESULTDATA.containing_type = _COCOINGEARRESULT
_COCOINGEARRESULT.fields_by_name['data'].message_type = _COCOINGEARRESULT_COCOINGEARRESULTDATA
_COCOINGEARRESULT.fields_by_name['exchangeResultData'].message_type = Exchange_pb2._EXCHANGERESULT_EXCHANGERESULTDATA
DESCRIPTOR.message_types_by_name['CocoinGearRequest'] = _COCOINGEARREQUEST
DESCRIPTOR.message_types_by_name['CocoinGearResult'] = _COCOINGEARRESULT

CocoinGearRequest = _reflection.GeneratedProtocolMessageType('CocoinGearRequest', (_message.Message,), dict(
  DESCRIPTOR = _COCOINGEARREQUEST,
  __module__ = 'CocoinGearQuery_pb2'
  # @@protoc_insertion_point(class_scope:CocoinGearRequest)
  ))
_sym_db.RegisterMessage(CocoinGearRequest)

CocoinGearResult = _reflection.GeneratedProtocolMessageType('CocoinGearResult', (_message.Message,), dict(

  CocoinGearInfo = _reflection.GeneratedProtocolMessageType('CocoinGearInfo', (_message.Message,), dict(
    DESCRIPTOR = _COCOINGEARRESULT_COCOINGEARINFO,
    __module__ = 'CocoinGearQuery_pb2'
    # @@protoc_insertion_point(class_scope:CocoinGearResult.CocoinGearInfo)
    ))
  ,

  CocoinGearResultData = _reflection.GeneratedProtocolMessageType('CocoinGearResultData', (_message.Message,), dict(
    DESCRIPTOR = _COCOINGEARRESULT_COCOINGEARRESULTDATA,
    __module__ = 'CocoinGearQuery_pb2'
    # @@protoc_insertion_point(class_scope:CocoinGearResult.CocoinGearResultData)
    ))
  ,
  DESCRIPTOR = _COCOINGEARRESULT,
  __module__ = 'CocoinGearQuery_pb2'
  # @@protoc_insertion_point(class_scope:CocoinGearResult)
  ))
_sym_db.RegisterMessage(CocoinGearResult)
_sym_db.RegisterMessage(CocoinGearResult.CocoinGearInfo)
_sym_db.RegisterMessage(CocoinGearResult.CocoinGearResultData)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.oppo.pay.bean'))
# @@protoc_insertion_point(module_scope)
