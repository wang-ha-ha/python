# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Msg

import flatbuffers

class Payload(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsPayload(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Payload()
        x.Init(buf, n + offset)
        return x

    # Payload
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Payload
    def PayloadType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Payload
    def Payload(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def PayloadStart(builder): builder.StartObject(2)
def PayloadAddPayloadType(builder, payloadType): builder.PrependUint8Slot(0, payloadType, 0)
def PayloadAddPayload(builder, payload): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(payload), 0)
def PayloadEnd(builder): return builder.EndObject()
