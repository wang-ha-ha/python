# automatically generated by the FlatBuffers compiler, do not modify

# namespace: msg

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class RouteInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RouteInfo()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsRouteInfo(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # RouteInfo
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # RouteInfo
    def Countx(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # RouteInfo
    def County(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # RouteInfo
    def Routeid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # RouteInfo
    def Reply(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # RouteInfo
    def Result(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # RouteInfo
    def Reason(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def Start(builder): builder.StartObject(6)
def RouteInfoStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddCountx(builder, countx): builder.PrependInt32Slot(0, countx, 0)
def RouteInfoAddCountx(builder, countx):
    """This method is deprecated. Please switch to AddCountx."""
    return AddCountx(builder, countx)
def AddCounty(builder, county): builder.PrependInt32Slot(1, county, 0)
def RouteInfoAddCounty(builder, county):
    """This method is deprecated. Please switch to AddCounty."""
    return AddCounty(builder, county)
def AddRouteid(builder, routeid): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(routeid), 0)
def RouteInfoAddRouteid(builder, routeid):
    """This method is deprecated. Please switch to AddRouteid."""
    return AddRouteid(builder, routeid)
def AddReply(builder, reply): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(reply), 0)
def RouteInfoAddReply(builder, reply):
    """This method is deprecated. Please switch to AddReply."""
    return AddReply(builder, reply)
def AddResult(builder, result): builder.PrependInt8Slot(4, result, 0)
def RouteInfoAddResult(builder, result):
    """This method is deprecated. Please switch to AddResult."""
    return AddResult(builder, result)
def AddReason(builder, reason): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(reason), 0)
def RouteInfoAddReason(builder, reason):
    """This method is deprecated. Please switch to AddReason."""
    return AddReason(builder, reason)
def End(builder): return builder.EndObject()
def RouteInfoEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)