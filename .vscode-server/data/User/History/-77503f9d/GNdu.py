"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

# try:
#     import cStringIO.StringIO as BytesIO
# except ImportError:
from io import BytesIO
import struct

class localization_lcmt(object):
    __slots__ = ["xyz", "vxyz", "rpy", "omegaBody", "vBody", "timestamp"]

    __typenames__ = ["float", "float", "float", "float", "float", "int64_t"]

    __dimensions__ = [[3], [3], [3], [3], [3], None]

    def __init__(self):
        self.xyz = [ 0.0 for dim0 in range(3) ]
        self.vxyz = [ 0.0 for dim0 in range(3) ]
        self.rpy = [ 0.0 for dim0 in range(3) ]
        self.omegaBody = [ 0.0 for dim0 in range(3) ]
        self.vBody = [ 0.0 for dim0 in range(3) ]
        self.timestamp = 0

    def encode(self):
        buf = BytesIO()
        buf.write(localization_lcmt._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack('>3f', *self.xyz[:3]))
        buf.write(struct.pack('>3f', *self.vxyz[:3]))
        buf.write(struct.pack('>3f', *self.rpy[:3]))
        buf.write(struct.pack('>3f', *self.omegaBody[:3]))
        buf.write(struct.pack('>3f', *self.vBody[:3]))
        buf.write(struct.pack(">q", self.timestamp))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != localization_lcmt._get_packed_fingerprint():
            raise ValueError("Decode error")
        return localization_lcmt._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = localization_lcmt()
        self.xyz = struct.unpack('>3f', buf.read(12))
        self.vxyz = struct.unpack('>3f', buf.read(12))
        self.rpy = struct.unpack('>3f', buf.read(12))
        self.omegaBody = struct.unpack('>3f', buf.read(12))
        self.vBody = struct.unpack('>3f', buf.read(12))
        self.timestamp = struct.unpack(">q", buf.read(8))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if localization_lcmt in parents: return 0
        tmphash = (0x7e246f0371a27d89) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if localization_lcmt._packed_fingerprint is None:
            localization_lcmt._packed_fingerprint = struct.pack(">Q", localization_lcmt._get_hash_recursive([]))
        return localization_lcmt._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", localization_lcmt._get_packed_fingerprint())[0]

