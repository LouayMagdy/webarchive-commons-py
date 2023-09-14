import os
import sys
import mmap

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from streamcontext.AbstractBufferingStream import AbstractBufferingStream, _DEFAULT_READ_SIZE


# Random Access File is replaced with Memory mapped I/O file (mmap)


class RandomAccessFileStream(AbstractBufferingStream):
    def __init__(self, file, offset: int = 0, read_size: int = _DEFAULT_READ_SIZE):
        super().__init__(offset, read_size)
        self._random_access_file = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ)
        self._file = file
        self._pointer = offset  # DO NOT WORRY! super constructor checks if offset is negative

    def get_file(self):
        return self._file

    def do_close(self):
        self._random_access_file.close()

    def do_read(self, b: bytearray, offset: int, length: int) -> int:
        try:
            amt_to_read = min(length, os.fstat(self._file.fileno()).st_size - self._pointer)
            if amt_to_read > len(b) - offset:
                raise IndexError("Index out of bound Exception")
            b[offset: offset + amt_to_read] = self._random_access_file[self._pointer: self._pointer + amt_to_read]
            self._pointer += amt_to_read
            return amt_to_read if amt_to_read > 0 else -1
        except Exception as e:
            raise IOError() from e

    def do_seek(self, offset: int):
        try:
            if offset < 0 or offset > os.fstat(self._file.fileno()).st_size:
                raise IOError("Index out of Bound Exception")
            self._pointer = offset
        except (IndexError, ValueError):
            raise IOError("Index out of Bound Exception")
