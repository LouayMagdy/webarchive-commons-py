import threading
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from utils.PushBackOneByteInputStream import PushBackOneByteInputStream
from streamcontext.Stream import Stream

mark_lock = threading.Lock()
reset_lock = threading.Lock()


class StreamWrappedInputStream(PushBackOneByteInputStream):
    _un_marked = -1

    def __init__(self, stream: Stream):
        self.stream = stream
        self.mark_pos = self._un_marked
        self.close_on_close = False

    def set_close_on_close(self, close_on_close: bool):
        self.close_on_close = close_on_close

    def is_close_on_close(self) -> bool:
        return self.close_on_close

    def available(self) -> int:
        return 0

    def close(self):
        if self.close_on_close:
            self.stream.close()

    def mark(self, read_limit):
        with mark_lock:
            self.mark_pos = self.stream.get_offset()

    def is_mark_supported(self) -> bool:
        return True

    def reset(self):
        with reset_lock:
            if self.mark_pos == self._un_marked:
                raise IOError("Reset without mark() unsupported")
            self.stream.set_offset(self.mark_pos)
            self.mark_pos = self._un_marked

    def read(self, byte_arr=None, offset=0, length=None) -> int:
        if byte_arr is not None:
            if length is None:
                length = len(byte_arr)
            return self.stream.read(byte_arr, offset, length)
        b = bytearray(1)
        amt = self.stream.read(b, 0, 1)
        return -1 if amt == -1 else b[0] & 0xFF

    def skip(self, n_bytes) -> int:
        if n_bytes < 1:
            return 0
        start_offset = self.stream.get_offset()
        got_offset = self.stream.set_offset(start_offset + n_bytes)
        return got_offset - start_offset

    def push_back(self):
        self.stream.set_offset(self.stream.get_offset() - 1)
