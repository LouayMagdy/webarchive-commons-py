import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from utils.CRC32 import CRC32


class CRCInputStream:
    def __init__(self, input_stream, crc: CRC32 = CRC32()):
        self._input_stream = input_stream
        self._crc = crc
        self._count = 0

    def read(self, buffer: bytearray = None, offset: int = 0, length: int = None):
        if buffer is None and length is None:
            # this is to dread on byte
            b = self._input_stream.read()
            if b != -1:
                self._crc.update(b)
                self._count += 1
            return b
        elif buffer is not None:
            # here buffer is provided but length should be deduced from len(buffer)
            if length is None:
                length = len(buffer)
            buffer[offset:] = bytearray(self._input_stream.read(length=length))
            amount = len(buffer) - offset
            if amount > -1:
                self._crc.update(buffer[offset: offset + amount])
                self._count += amount
            return amount
        else:
            # length is provided. go and read length bytes then return byte array
            return bytearray(self._input_stream.read(length=length))

    def get_crc_value(self):
        return self._crc.get_value()

    def get_byte_count(self):
        return self._count

    # the following methods are because this class is supposed to implement InputStream class
    def tell(self) -> int:
        return self._input_stream.tell()

    def seek(self, pos: int):
        self._input_stream.seek(pos)

    def fileno(self):
        return self._input_stream.fileno()