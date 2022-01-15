# PyHill - A brick-hill client in python, by Malte0621. #
# - Helper : Commonly used functions.

import struct
import zlib


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


class Properties:
    def __init__(self, ret):
        self.ret = ret

    def __getitem__(self, item):
        return self.ret[item]

    def __getattr__(self, item):
        if item == "keys":
            return self.ret.keys
        elif item == "values":
            return self.ret.values
        return self.ret[item]


def unpack_helper(fmt, data):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[:size]), data[size:]


class Packet:
    def __init__(self, packetId):
        if type(packetId) == int:
            self.buffer = struct.pack("<B", packetId)
        else:
            self.buffer = packetId

    def compress(self):
        self.buffer = zlib.compress(self.buffer, level=9)

    def decompress(self):
        self.buffer = zlib.decompress(self.buffer)

    def write_string(self, value):
        self.buffer += value + b"\x00"

    def write_bool(self, value):
        self.buffer += struct.pack("?", value)

    def write_float(self, value):
        self.buffer += struct.pack("<f", value)

    def write_int8(self, value):
        self.buffer += struct.pack("<b", value)

    def write_uint8(self, value):
        self.buffer += struct.pack("<B", value)

    def write_int32(self, value):
        self.buffer += struct.pack("<i", value)

    def write_uint32(self, value):
        self.buffer += struct.pack("<I", value)

    def write_int16(self, value):
        self.buffer += struct.pack("<h", value)

    def write_uint16(self, value):
        self.buffer += struct.pack("<H", value)

    def write_long(self, value):
        self.buffer += struct.pack("<l", value)

    def read_string(self):
        s = self.buffer.split(b"\x00")
        try:
            self.buffer = b"\x00".join(s[1:])
        except:
            pass
        return s[0]

    def read_bool(self):
        r = struct.unpack("?", self.buffer[0:struct.calcsize("?")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("?"):]
        except:
            pass
        return r

    def read_float(self):
        r = struct.unpack("<f", self.buffer[0:struct.calcsize("<f")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<f"):]
        except:
            pass
        return r

    def read_int8(self):
        r = struct.unpack("<b", self.buffer[0:struct.calcsize("<b")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<b"):]
        except:
            pass
        return r

    def read_uint8(self):
        r = struct.unpack("<B", self.buffer[0:struct.calcsize("<B")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<B"):]
        except:
            pass
        return r

    def read_int16(self):
        r = struct.unpack("<h", self.buffer[0:struct.calcsize("<h")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<h"):]
        except:
            pass
        return r

    def read_uint16(self):
        r = struct.unpack("<H", self.buffer[0:struct.calcsize("<H")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<H"):]
        except:
            pass
        return r

    def read_int32(self):
        r = struct.unpack("<i", self.buffer[0:struct.calcsize("<i")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<i"):]
        except:
            pass
        return r

    def read_uint32(self):
        r = struct.unpack("<I", self.buffer[0:struct.calcsize("<I")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<I"):]
        except:
            pass
        return r

    def read_long(self):
        r = struct.unpack("<l", self.buffer[0:struct.calcsize("<l")])[0]
        try:
            self.buffer = self.buffer[struct.calcsize("<l"):]
        except:
            pass
        return r
