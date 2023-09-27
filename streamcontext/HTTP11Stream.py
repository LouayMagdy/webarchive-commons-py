import urllib.request
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from streamcontext.AbstractBufferingStream import AbstractBufferingStream, _DEFAULT_READ_SIZE


class HTTP11Stream(AbstractBufferingStream):
    def __init__(self, url_str: str, offset: int = 0, read_size: int = _DEFAULT_READ_SIZE):
        super().__init__(offset, read_size)
        self._url = url_str
        self._url_connection = None
        self._input_stream = None
        self.do_seek(offset)

    def do_read(self, b: bytearray, offset: int, length: int) -> int:
        if length > len(b) - offset:
            raise IOError('Index out of bound Exception')
        amt_read_via_http = self._input_stream.readinto(memoryview(b)[offset: offset + length])
        return -1 if amt_read_via_http == 0 else amt_read_via_http

    def do_seek(self, offset: int):
        try:
            if offset < 0:
                raise IndexError("Index Out of Bound Exception")
            self.do_close()
            request = urllib.request.Request(self._url, headers={"Range": f"bytes={offset}-"})
            self._url_connection = urllib.request.urlopen(request)
            self._input_stream = self._url_connection.fp.raw
        except Exception as e:
            raise IOError() from e

    def do_close(self):
        try:
            if self._input_stream:
                self._input_stream.close()
                self._input_stream = None
        except Exception as e:
            raise IOError() from e
