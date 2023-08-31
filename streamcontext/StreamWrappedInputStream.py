import threading
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from utils.PushBackOneByteInputStream import PushBackOneByteInputStream

mark_lock = threading.Lock()
reset_lock = threading.Lock()


class StreamWrappedInputStream(PushBackOneByteInputStream):
    _un_marked = -1

    def __init__(self, stream):  # stream is considered as a file stream --> see the commented example below
        self.stream = stream
        self.mark_pos = self._un_marked
        self.close_on_close = False
        self._read_limit = self._un_marked

    def set_close_on_close(self, close_on_close):
        self.close_on_close = close_on_close

    def is_close_on_close(self):
        return self.close_on_close

    def available(self):
        return 0

    def close(self):
        if self.close_on_close:
            self.stream.close()

    def mark(self, read_limit):
        with mark_lock:
            self.mark_pos = self.stream.tell()
            self._read_limit = read_limit

    def is_mark_supported(self):
        return True

    def reset(self):
        with reset_lock:
            if self.mark_pos == self._un_marked:
                raise IOError("Reset without mark() unsupported")
            self.stream.seek(self.mark_pos)
            self.mark_pos = self._un_marked
            self._read_limit = self._un_marked

    def read(self, byte_arr=None, offset=None, length=None):
        if offset is None:
            offset = 0
        if length is None and byte_arr is not None:
            length = len(byte_arr)
        if byte_arr is None:
            length = 1
            byte_arr = bytearray(1)
        if self.mark_pos != self._un_marked:
            self._read_limit -= length
            if self._read_limit <= 0:
                self.mark_pos = self._un_marked
        self.stream.seek(offset)
        byte_arr[:] = bytearray(self.stream.read(length))
        return byte_arr[0] & 0xff if length == len(byte_arr) == 1 else None

    def skip(self, n_bytes):
        if n_bytes < 1:
            return 0
        start_offset = self.stream.tell()
        got_offset = self.stream.seek(start_offset + n_bytes)
        return got_offset - start_offset

    def push_back(self):
        self.stream.seek(self.stream.tell() - 1)

# with open("./experimental/my_dict.json", "rb") as f_i:
#     swis = StreamWrappedInputStream(f_i)
#     with open("offset_stream.txt", "w") as f_o:
#         f_i.seek(200)
#         print(f"offset: {f_i.tell()}")
#         buff = f_i.read().decode()
#         print(buff)
#         f_o.write(buff)
#
# with open("./experimental/my_dict.json", "rb") as f_i:
#     swis2 = StreamWrappedInputStream(f_i)
#     with open("stream.txt", "wb") as f_o:
#         buff = bytearray(10) # for the next to lines only
# #         # swis2.read(buff, 200, 10)
#         swis2.read(buff)
# #         buff = swis2.read()
#         print(buff)
#         # f_o.write(buff)

# with open("./experimental/my_dict.json", "rb") as f_i1:
#     swis3 = StreamWrappedInputStream(f_i1)
#     swis3.skip(10)
#     swis3.mark(2)
#     print(f"{swis3.read()} --- forget after {swis3._read_limit} -- {swis3._un_marked}")
#     swis3.reset()
#     swis3.mark(7)
#     buff = bytearray(7)
#     swis3.read(buff, 7)
#     print(f"{buff} --- forget after {swis3._read_limit} -- {swis3._un_marked}")
#     swis3.reset()
