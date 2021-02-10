# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: NoticePb.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


<<<<<<< HEAD
from lib.pb_src.python_native import BaseResult_pb2
from lib.pb_src.python_native import BaseHeader_pb2
=======
from . import BaseResult_pb2
from . import BaseHeader_pb2
>>>>>>> 4e34fc7b73277790c2a238e3f3e548ca076d215e

DESCRIPTOR = _descriptor.FileDescriptor(
  name='NoticePb.proto',
  package='Notice',
  serialized_pb=_b('\n\x0eNoticePb.proto\x12\x06Notice\x1a\x10\x42\x61seHeader.proto\x1a\x10\x42\x61seResult.proto\"\xbf\x01\n\x07Request\x12&\n\x06header\x18\x01 \x02(\x0b\x32\x16.BaseHeader.BaseHeader\x12\x16\n\x0e\x63ontactVersion\x18\x02 \x02(\t\x12\x16\n\x0espeakerVersion\x18\x03 \x02(\t\x12(\n\x07\x63hannel\x18\x04 \x01(\x0e\x32\x17.Notice.Request.Channel\x12\x0c\n\x04sign\x18\x05 \x02(\t\"$\n\x07\x43hannel\x12\x07\n\x03_0P\x10\x00\x12\x07\n\x03_1P\x10\x01\x12\x07\n\x03_2P\x10\x02\"\xd9\x01\n\x06Result\x12\x15\n\rcontactStatus\x18\x01 \x02(\t\x12\x15\n\rspeakerStatus\x18\x02 \x02(\t\x12\x0f\n\x07\x63ontact\x18\x03 \x01(\t\x12\x12\n\ncontactTel\x18\x04 \x01(\t\x12\x16\n\x0e\x63ontactVersion\x18\x05 \x01(\t\x12 \n\x07speaker\x18\x06 \x03(\x0b\x32\x0f.Notice.Speaker\x12\x16\n\x0espeakerVersion\x18\x07 \x01(\t\x12*\n\nbaseresult\x18\x08 \x01(\x0b\x32\x16.BaseResult.BaseResult\"?\n\x07Speaker\x12\x0c\n\x04page\x18\x01 \x02(\t\x12&\n\nspeakerMsg\x18\x02 \x03(\x0b\x32\x12.Notice.SpeakerMsg\"A\n\nSpeakerMsg\x12\x0f\n\x07\x63ontent\x18\x01 \x02(\t\x12\x11\n\tstartTime\x18\x02 \x02(\t\x12\x0f\n\x07\x65ndTime\x18\x03 \x02(\tB#\n\x11\x63om.nearme.pluginB\x0eNoticePbEntity')
  ,
  dependencies=[BaseHeader_pb2.DESCRIPTOR,BaseResult_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_REQUEST_CHANNEL = _descriptor.EnumDescriptor(
  name='Channel',
  full_name='Notice.Request.Channel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='_0P', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='_1P', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='_2P', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=218,
  serialized_end=254,
)
_sym_db.RegisterEnumDescriptor(_REQUEST_CHANNEL)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Notice.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Notice.Request.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='contactVersion', full_name='Notice.Request.contactVersion', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speakerVersion', full_name='Notice.Request.speakerVersion', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channel', full_name='Notice.Request.channel', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign', full_name='Notice.Request.sign', index=4,
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
    _REQUEST_CHANNEL,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=63,
  serialized_end=254,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Notice.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='contactStatus', full_name='Notice.Result.contactStatus', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speakerStatus', full_name='Notice.Result.speakerStatus', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='contact', full_name='Notice.Result.contact', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='contactTel', full_name='Notice.Result.contactTel', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='contactVersion', full_name='Notice.Result.contactVersion', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speaker', full_name='Notice.Result.speaker', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speakerVersion', full_name='Notice.Result.speakerVersion', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baseresult', full_name='Notice.Result.baseresult', index=7,
      number=8, type=11, cpp_type=10, label=1,
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
  serialized_start=257,
  serialized_end=474,
)


_SPEAKER = _descriptor.Descriptor(
  name='Speaker',
  full_name='Notice.Speaker',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='page', full_name='Notice.Speaker.page', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speakerMsg', full_name='Notice.Speaker.speakerMsg', index=1,
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
  serialized_start=476,
  serialized_end=539,
)


_SPEAKERMSG = _descriptor.Descriptor(
  name='SpeakerMsg',
  full_name='Notice.SpeakerMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='content', full_name='Notice.SpeakerMsg.content', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='startTime', full_name='Notice.SpeakerMsg.startTime', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endTime', full_name='Notice.SpeakerMsg.endTime', index=2,
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
  serialized_start=541,
  serialized_end=606,
)

_REQUEST.fields_by_name['header'].message_type = BaseHeader_pb2._BASEHEADER
_REQUEST.fields_by_name['channel'].enum_type = _REQUEST_CHANNEL
_REQUEST_CHANNEL.containing_type = _REQUEST
_RESULT.fields_by_name['speaker'].message_type = _SPEAKER
_RESULT.fields_by_name['baseresult'].message_type = BaseResult_pb2._BASERESULT
_SPEAKER.fields_by_name['speakerMsg'].message_type = _SPEAKERMSG
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['Speaker'] = _SPEAKER
DESCRIPTOR.message_types_by_name['SpeakerMsg'] = _SPEAKERMSG

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'NoticePb_pb2'
  # @@protoc_insertion_point(class_scope:Notice.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'NoticePb_pb2'
  # @@protoc_insertion_point(class_scope:Notice.Result)
  ))
_sym_db.RegisterMessage(Result)

Speaker = _reflection.GeneratedProtocolMessageType('Speaker', (_message.Message,), dict(
  DESCRIPTOR = _SPEAKER,
  __module__ = 'NoticePb_pb2'
  # @@protoc_insertion_point(class_scope:Notice.Speaker)
  ))
_sym_db.RegisterMessage(Speaker)

SpeakerMsg = _reflection.GeneratedProtocolMessageType('SpeakerMsg', (_message.Message,), dict(
  DESCRIPTOR = _SPEAKERMSG,
  __module__ = 'NoticePb_pb2'
  # @@protoc_insertion_point(class_scope:Notice.SpeakerMsg)
  ))
_sym_db.RegisterMessage(SpeakerMsg)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021com.nearme.pluginB\016NoticePbEntity'))
# @@protoc_insertion_point(module_scope)
