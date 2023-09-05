import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from utils.ByteOp import *

class GZIPStaticHeader:
    _GZIP_STATIC_HEADER_SIZE_MINUS_3 = GZIPConstants.get('GZIP_STATIC_HEADER_SIZE') - 3
    _DEFAULT_HEADER_DATA = bytearray([
        GZIPConstants.get('GZIP_MAGIC_ONE') & 0xff,
        GZIPConstants.get('GZIP_MAGIC_TWO') & 0xff,
        GZIPConstants.get('GZIP_COMPRESSION_METHOD_DEFLATE') & 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03])

    def __init__(self, input_stream=None, assume1st3:bool=None):
        self._data = copy(self._DEFAULT_HEADER_DATA)
        if input_stream is not None and assume1st3 is not None:
            amt = input_stream.read(self._data, 3, self._GZIP_STATIC_HEADER_SIZE_MINUS_3)
            if amt != self._GZIP_STATIC_HEADER_SIZE_MINUS_3
                raise
            self.validate_buffer()

    def validate_buffer(self):
        return


