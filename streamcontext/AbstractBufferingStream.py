import sys
import os
from abc import abstractmethod

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from streamcontext.Stream import Stream


class AbstractBufferingStream(Stream):  # implementing a bulk of methods except 3 methods left for the subclasses
    _DEFAULT_READ_SIZE = 4096

    def __init__(self, offset: int = 0, read_size: int = _DEFAULT_READ_SIZE):
        if offset < 0:
            raise IndexError("Index Out of Bound Exception")
        self._offset = offset
        self._buffer = bytearray(read_size)
        self._closed = False
        self._at_eof = False
        self._buffer_remaining = 0
        self._buffer_cursor = 0

    @abstractmethod
    def do_read(self, b: bytearray, offset: int, length: int) -> int:
        pass

    @abstractmethod
    def do_seek(self, offset: int):
        pass

    @abstractmethod
    def do_close(self):
        pass

    def is_at_eof(self) -> bool:
        return self._at_eof

    def get_offset(self) -> int:
        return self._offset

    def read(self, b: bytearray, offset: int, length: int) -> int:
        if self._closed:
            raise IOError("Read after close()")
        if self._at_eof:
            return -1
        amt_read = 0
        while length > 0:
            if self._buffer_remaining > 0:
                amt_to_copy = min(length, self._buffer_remaining)
                b[offset: offset + amt_to_copy] = self._buffer[self._buffer_cursor: self._buffer_cursor + amt_to_copy]
                self._buffer_cursor += amt_to_copy
                self._buffer_remaining -= amt_to_copy
                offset += amt_to_copy
                length -= amt_to_copy
                amt_read += amt_to_copy
                # note that now: Either the read is satisfied or the buffer gets empty or both
            if length > 0:  # let's fill the buffer again
                amt_read_now = self.do_read(self._buffer, 0, len(self._buffer))
                if amt_read_now == -1:
                    self._at_eof = True
                    break
                self._buffer_cursor = 0
                self._buffer_remaining = amt_read_now
        if not amt_read:  # we are at eof
            amt_read = -1
        else:  # advance the offset
            self._offset += amt_read
        return amt_read

    def set_offset(self, offset: int) -> int:
        if self._offset < offset:  # seeking forward
            amt_to_skip = offset - self._offset
            if amt_to_skip < self._buffer_remaining:  # skipping to somewhere in our current buffer
                self._buffer_remaining -= amt_to_skip
                self._buffer_cursor += amt_to_skip
            else:  # seeking forward beyond buffer
                self.do_seek(offset)
                self._buffer_remaining = 0
            self._at_eof = False
        elif self._offset > offset:  # seeking backward
            amt_to_reverse = self._offset - offset
            if self._buffer_cursor > amt_to_reverse:  #within our buffer
                self._buffer_cursor -= amt_to_reverse
                self._buffer_remaining += amt_to_reverse
            else:  # beyond the buffer
                self.do_seek(offset)
                self._buffer_remaining = 0
            self._at_eof = False
        self._offset = offset
        return offset

    def close(self):
        if not self._closed:
            self.do_close()
            self._closed = True
