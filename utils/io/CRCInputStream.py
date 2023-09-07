import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from utils.CRC32 import CRC32


class CRCInputStream:
    def __init__(self, input_stream, crc: CRC32 = CRC32()):
        self._input_stream = input_stream
        self._crc = crc
        self._count = 0

    def read_byte(self) -> int:
        b = self._input_stream.read()
        if b != -1:
            self._crc.update(b)
            self._count += 1
        return b

    def read_byte_arr(self, buffer: bytearray, offset: int = 0, length: int = None) -> int:
        if length is None:
            length = len(buffer)
        amount = self._input_stream.read(buffer, offset, length)
        if amount > -1:
            self._crc.update(buffer[offset: offset + amount])
            self._count += amount
        return amount

    def get_crc_value(self):
        return self._crc.get_value()

    def get_byte_count(self):
        return self._count
