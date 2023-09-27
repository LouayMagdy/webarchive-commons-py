import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPFormatException import GZIPFormatException, GZIPExtraFieldShortException
from utils.ByteOp import *


class GZIPFExtraRecord:
    def __init__(self, name: bytearray = None, value: bytearray = None, int_val=None):
        if name is None:
            # this means that all is None
            return
        if len(name) != GZIPConstants.get("GZIP_FEXTRA_NAME_BYTES"):
            raise GZIPFormatException("FExtra name is 2 bytes")
        self._name = name
        if value is not None and len(value) > GZIPConstants.get("GZIP_FEXTRA_VALUE_MAX_LENGTH"):
            raise GZIPFormatException(f"FExtra value max is {GZIPConstants.get('GZIP_FEXTRA_VALUE_MAX_LENGTH')} bytes")
        self._value = value
        if int_val is not None:
            self._value = bytearray(4)
            write_int(int_val=int_val, buffer=self._value)

    def matches_name(self, name: bytearray) -> bool:
        if name is None or self._name is None:
            return False
        return cmp(self._name, name)

    def get_name(self) -> bytearray:
        return self._name

    def get_value(self) -> bytearray:
        return self._value

    def set_value(self, value: bytearray):
        self._value = value

    def length(self) -> int:
        if self._name is None:
            return 0
        if self._value is None:
            return GZIPConstants.get("GZIP_FEXTRA_VALUE_IDX")
        return GZIPConstants.get("GZIP_FEXTRA_VALUE_IDX") + len(self._value)

    def write_to(self, output_stream=None, buffer: bytearray = None, offset: int = None):
        if output_stream is None:
            if len(buffer) - offset < self.length():
                raise IndexError('Index out of range.')
            buffer[offset], buffer[offset + 1] = self._name[0], self._name[1]
            offset += GZIPConstants.get('GZIP_FEXTRA_LENGTH_IDX')
            if self._value is None:
                write_short(short_val=0, offset=offset, buffer=buffer)
            else:
                write_short(short_val=len(self._value), offset=offset, buffer=buffer)
                offset += GZIPConstants.get('GZIP_FEXTRA_LENGTH_BYTES')
                buffer[offset: offset + len(self._value)] = self._value[:len(self._value)]
        else:
            if self._name is None or self._value is None:
                return
            output_stream.write(self._name)
            if self._value is None:
                write_short(short_val=0, output_stream=output_stream)
            else:
                write_short(short_val=len(self._value), output_stream=output_stream)
                output_stream.write(self._value)

    def read(self, input_stream=None, max_to_read: int = None, buffer: bytearray = None, offset: int = None):
        tmp_name, tmp_val, val_len = None, None, 0
        if input_stream is not None:
            tmp_name = read_n_bytes(input_stream, GZIPConstants.get("GZIP_FEXTRA_NAME_BYTES"))
            val_len = read_short(input_stream)
            n = max_to_read - GZIPConstants.get("BYTES_IN_SHORT") - GZIPConstants.get("GZIP_FEXTRA_NAME_BYTES")
            if val_len > n:
                tmp_val = read_n_bytes(input_stream, n)
                raise GZIPExtraFieldShortException(max_to_read)
            if val_len > 0:
                tmp_val = read_n_bytes(input_stream, val_len)
            self._name, self._value = tmp_name, tmp_val
            return val_len - (n - max_to_read)
            # length of read field
        else:
            remaining = len(buffer) - offset
            if remaining < GZIPConstants.get("GZIP_FEXTRA_VALUE_IDX"):
                raise GZIPFormatException("Short bytes for FExtra field")
            tmp_name = copy(buffer, offset, GZIPConstants.get("GZIP_FEXTRA_NAME_BYTES"))
            val_len = bytes_to_short(byte_arr=buffer, offset=offset + GZIPConstants.get("GZIP_FEXTRA_LENGTH_IDX"))
            remaining -= GZIPConstants.get('GZIP_FEXTRA_NAME_IDX')
            if val_len > 0:
                if val_len > remaining:
                    raise GZIPFormatException("Short bytes for FExtra field")
                tmp_val = copy(buffer, offset + GZIPConstants.get("GZIP_FEXTRA_VALUE_IDX"), val_len)
            self._name, self._value = tmp_name, tmp_val
            return GZIPConstants.get("GZIP_FEXTRA_VALUE_IDX") + val_len

# t = GZIPFExtraRecord(bytearray([23, 45]), bytearray([12, 56, 89, 71, 89]))
# # t = GZIPFExtraRecord(name=bytearray([23, 45]), int_val=1)
# print(t.get_name(), t.get_value())
# print(t.matches_name(bytearray([23, 45])), t.matches_name(name=None), t.matches_name(bytearray([21])))
# print(t.length())
# buff = bytearray(15)
# t.write_to(buffer=buff, offset=0)
# print(buff)
# with open('./experimental/writing_short.txt', 'wb') as f_o:
#     t.write_to(f_o)
# with open('./experimental/writing_short.txt', "rb") as f_i:
#     t1 = GZIPFExtraRecord()
#     remain = t1.read(f_i, max_to_read=20)
#     print(t1.get_name(), t1.get_value(), remain)
# print(len(buff))
# print(t.read(buffer=buff, offset=0))
# print(t.get_name(), t.get_value())
# print(t.matches_name(bytearray([23, 45])), t.matches_name(name=None), t.matches_name(bytearray([21])))
# print(t.length())
