import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPFormatException import *
from utils.ByteOp import *


class GZIPFooter:
    def __init__(self, buffer: bytearray = None, crc: int = None, length: int = None):
        if buffer is not None:
            if len(buffer) != GZIPConstants.get("GZIP_FOOTER_BYTES"):
                self.buffer = None
                raise GZIPFormatException("Wrong length footer")
            self.buffer = buffer
        else:
            # crc and length are provided
            self.buffer = bytearray(GZIPConstants.get("GZIP_FOOTER_BYTES"))
            write_int(buffer=self.buffer, offset=0, int_val=crc)
            write_int(buffer=self.buffer, offset=GZIPConstants.get("BYTES_IN_INT"), int_val=length)

    def get_crc(self) -> int:
        return bytes_to_int(byte_arr=self.buffer, offset=0)

    def get_length(self) -> int:
        return bytes_to_int(byte_arr=self.buffer, offset=GZIPConstants.get("BYTES_IN_INT"))

    def verify(self, crc: int, length: int):
        want_crc_i = int(crc & 0xFFFFFFFF)
        if want_crc_i != self.get_crc():
            raise GZIPFormatException("GZip crc error")
        if length != self.get_length():
            raise GZIPFormatException("GZip length error")

    def write_bytes(self, output_stream):
        output_stream.write(self.buffer)


# # g_footer = GZIPFooter(buffer=bytearray([12, 13, 14, 15, 12, 13, 14, 15, 12, 13, 14, 15, 12, 13, 14, 15]))
# g_footer = GZIPFooter(crc=245, length=1478)
# print(g_footer.buffer)
# print(g_footer.get_crc())
# print(g_footer.get_length())
# print(g_footer.verify(g_footer.get_crc(), g_footer.get_length()))
# with open("./experimental/testing_CRC.txt", 'wb') as f:
#     g_footer.write_bytes(f)