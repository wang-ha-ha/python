# automatically generated by the FlatBuffers compiler, do not modify

# namespace: msg

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Payload(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Payload()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsPayload(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Payload
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Payload
    def TypeType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Payload
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def Start(builder): builder.StartObject(2)
def PayloadStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddTypeType(builder, typeType): builder.PrependUint8Slot(0, typeType, 0)
def PayloadAddTypeType(builder, typeType):
    """This method is deprecated. Please switch to AddTypeType."""
    return AddTypeType(builder, typeType)
def AddType(builder, type): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(type), 0)
def PayloadAddType(builder, type):
    """This method is deprecated. Please switch to AddType."""
    return AddType(builder, type)
def End(builder): return builder.EndObject()
def PayloadEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)