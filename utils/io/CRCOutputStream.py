import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from utils.CRC32 import CRC32


class CRCOutputStream:
    def __init__(self, output_stream, auto_flush: bool = False):
        self.output_stream = output_stream
        self._crc_32 = CRC32()
        self.auto_flush = auto_flush
        self.bytes_written = 0

    def write_byte(self, b: int):
        ls_byte = b & 0xFF
        self._crc_32.update(num=ls_byte)
        self.output_stream.write(bytearray([ls_byte]))
        if self.auto_flush:
            self.output_stream.flush()
        self.bytes_written += 1

    def write_byte_arr(self, b: bytearray, offset: int = 0, length: int = None):
        if length is None:
            length = len(b)
        self._crc_32.update(byte_arr=b[offset: offset + length])
        self.output_stream.write(b[:length])
        if self.auto_flush:
            self.output_stream.flush()
        self.bytes_written += length

    def get_crc_value(self) -> int:
        return self._crc_32.get_value()

    def get_bytes_written(self) -> int:
        return self.bytes_written
