import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPFormatException import GZIPFormatException
from utils.ByteOp import *


class GZIPStaticHeader:
    _GZIP_STATIC_HEADER_SIZE_MINUS_3 = GZIPConstants.get('GZIP_STATIC_HEADER_SIZE') - 3
    _DEFAULT_HEADER_DATA = bytearray([
        GZIPConstants.get('GZIP_MAGIC_ONE') & 0xff,
        GZIPConstants.get('GZIP_MAGIC_TWO') & 0xff,
        GZIPConstants.get('GZIP_COMPRESSION_METHOD_DEFLATE') & 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03])

    def __init__(self, input_stream=None, assume1st3: bool = None, data: bytearray = None):
        if input_stream is not None and assume1st3 is None:
            try:
                self._data = read_n_bytes(input_stream, GZIPConstants.get('GZIP_STATIC_HEADER_SIZE'))
            except Exception as eof:
                raise GZIPFormatException("Short header") from eof
        elif data is None:
            self._data = copy(self._DEFAULT_HEADER_DATA)
            if input_stream is not None and assume1st3 is not None:
                amt = input_stream.read(self._data, 3, self._GZIP_STATIC_HEADER_SIZE_MINUS_3)
                if amt != self._GZIP_STATIC_HEADER_SIZE_MINUS_3:
                    raise GZIPFormatException("Short header")
        else:
            if len(data) != GZIPConstants.get('GZIP_STATIC_HEADER_SIZE'):
                raise GZIPFormatException("Short header")
            self._data = data
        self.validate_buffer()

    def get_length(self) -> int:
        return GZIPConstants.get('GZIP_STATIC_HEADER_SIZE')

    def write_to(self, output_stream=None, buffer: bytearray = None, offset: int = None):
        if output_stream is not None:
            output_stream.write(self._data)
        else:
            length = GZIPConstants.get('GZIP_STATIC_HEADER_SIZE')
            if len(buffer) - offset < length:
                raise IndexError('Index out of range.')
            buffer[offset: length + offset] = self._data[:length]

    def validate_buffer(self):
        if self._data[GZIPConstants.get("GZIP_MAGIC_ONE_IDX")] & 0xff != GZIPConstants.get("GZIP_MAGIC_ONE"):
            raise GZIPFormatException("bad magic 1")
        if self._data[GZIPConstants.get("GZIP_MAGIC_TWO_IDX")] & 0xff != GZIPConstants.get("GZIP_MAGIC_TWO"):
            raise GZIPFormatException("bad magic 2")
        if self._data[GZIPConstants.get("GZIP_COMPRESSION_METHOD_IDX")] & 0xff != GZIPConstants.get(
                "GZIP_COMPRESSION_METHOD_DEFLATE"):
            raise GZIPFormatException("bad compression method")
        flag = self._data[GZIPConstants.get("GZIP_FLAG_IDX")] & 0xff
        if (flag & GZIPConstants.get("GZIP_FLAG_VALID_BITS")) != flag:
            raise GZIPFormatException("bad flag bits")

    def set_flg(self, flag: int, val: bool):
        flag_idx = GZIPConstants.get("GZIP_FLAG_IDX")
        self._data[flag_idx] = (self._data[flag_idx] | flag) if val else (self._data[flag_idx] & ~flag)

    def is_flg_set(self, flag: int):
        return (self._data[GZIPConstants.get("GZIP_FLAG_IDX")] & flag) == flag

    def get_int_val(self, offset: int):
        return self._data[offset] & 0xff

    def get_os(self):
        return self.get_int_val(GZIPConstants.get("GZIP_OS_IDX"))

    def get_mtime(self):
        return bytes_to_int(byte_arr=self._data, offset=GZIPConstants.get("GZIP_MTIME_IDX"))

    def is_ftext_set(self):
        return self.is_flg_set(GZIPConstants.get("GZIP_FLAG_FTEXT"))

    def set_ftext_flag(self, val: bool):
        self.set_flg(GZIPConstants.get("GZIP_FLAG_FTEXT"), val)

    def is_fhcrc_set(self):
        return self.is_flg_set(GZIPConstants.get("GZIP_FLAG_FHCRC"))

    def set_fhcrc_flag(self, val: bool):
        self.set_flg(GZIPConstants.get("GZIP_FLAG_FHCRC"), val)

    def is_fextra_set(self):
        return self.is_flg_set(GZIPConstants.get("GZIP_FLAG_FEXTRA"))

    def set_fextra_flag(self, val: bool):
        self.set_flg(GZIPConstants.get("GZIP_FLAG_FEXTRA"), val)

    def is_fname_set(self):
        return self.is_flg_set(GZIPConstants.get("GZIP_FLAG_FNAME"))

    def set_fname_flag(self, val: bool):
        self.set_flg(GZIPConstants.get("GZIP_FLAG_FNAME"), val)

    def is_fcomment_set(self):
        return self.is_flg_set(GZIPConstants.get("GZIP_FLAG_FCOMMENT"))

    def set_fcomment_flag(self, val: bool):
        self.set_flg(GZIPConstants.get("GZIP_FLAG_FCOMMENT"), val)


# with open('./experimental/writing_short.txt', 'wb') as f_o:
#     byte_arr = bytearray([0x1f, 0x8b, 0x08, 3, 6, 7, 9, 42, 14, 26])
#
# with open(('./experimental/writing_short.txt'), 'rb') as f_i:
#     t = GZIPStaticHeader(f_i)
#
# t = GZIPStaticHeader(data=bytearray([0x1f, 0x8b, 0x08, 3, 6, 7, 9, 42, 14, 26]))
# t.set_flg(5, False)
# print(t._data, t.get_int_val(7), t.get_os(), t.get_mtime(), t.get_length())
# buffer = bytearray(15)
# t.write_to(buffer=buffer, offset=5)
# print(t._data, buffer)