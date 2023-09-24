from hdfs import InsecureClient
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from streamcontext.AbstractBufferingStream import AbstractBufferingStream, _DEFAULT_READ_SIZE

MAX_TO_READ=1024


class HDFSStream(AbstractBufferingStream):

    def __init__(self, server_url: str, file_path: str, offset: int = 0):
        self.client = InsecureClient(server_url)
        self.file_size = self.client.status(file_path)['length']
        self.file_path = file_path
        self.cursor_pos = offset
        self.input_stream = self.client.read(self.file_path, offset, MAX_TO_READ)

    def do_read(self, b: bytearray, offset: int, length: int) -> int:
        if length > len(b) - offset:
            raise IOError('Index out of bound Exception')
        if self.cursor_pos >= self.file_size or length <= 0:
            return -1
        sum_read, len_data = 0, 0
        with self.input_stream as _is:
            read_data = _is.read(min(length, MAX_TO_READ))
            len_data = len(read_data)
            b[offset: offset + len_data] = read_data[:]
            sum_read += len_data
        self.do_seek(self.cursor_pos + len_data)
        if MAX_TO_READ <= length and self.cursor_pos < self.file_size:
            sum_read += max(self.do_read(b, offset + len_data, length - len_data), 0)
        return sum_read

    def do_close(self):
        return

    def do_seek(self, offset: int):
        self.cursor_pos = offset
        self.input_stream = self.client.read(self.file_path, offset, MAX_TO_READ)

# s = HDFSStream("http://10.35.139.54:9870", "/text_files/text_1.txt")
# b = bytearray(608)
# print(s.do_read(b, 0, 500))
# print(b[:500])
# print(s.do_read(b, 500, 100))
# print(b[:600])
# print(s.do_read(b, 600, 8))
# print(b[:])
