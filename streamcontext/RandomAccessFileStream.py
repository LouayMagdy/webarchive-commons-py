import os
import sys
import mmap
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from streamcontext.AbstractBufferingStream import AbstractBufferingStream
# Random Access File is replaced with Memory mapped I/O file (mmap)


class RandomAccessFileStream(AbstractBufferingStream):
    def __init__(self, file, offset: int = 0, read_size: int = super()._DEFAULT_READ_SIZE):
        super().__init__(offset, read_size)
        self._random_access_file = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ)
        if offset > 0:
            # self._random_access_file.seek(offset)
            self._offset = offset
        self._file = file

    def get_file(self):
        return self._file

    def do_close(self):
        self._random_access_file.close()

    def do_read(self, b: bytearray, offset: int, length: int) -> int:
        try:
            amt_to_read = min(length, self._file.fileno - self._offset)
            if amt_to_read > len(b):
                raise IndexError("Index out of bound Exception")
            b[offset: offset + amt_to_read] = self._random_access_file[self._offset: self._offset + amt_to_read]
            return amt_to_read
        except Exception as e:
            raise IndexError() from e

    def do_seek(self, offset: int):
        try:
            self._offset = offset
        except Exception:
            raise IndexError("Index out of Bound Exception")
