import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants

class GZIPStaticHeader:
    _GZIP_STATIC_HEADER_SIZE_MINUS_3 = GZIPConstants.get('GZIP_STATIC_HEADER_SIZE') - 3
    _DEFAULT_HEADER_DATA = bytearray([
        GZIPConstants.get('GZIP_MAGIC_ONE') & 0xff,
        GZIPConstants.get('GZIP_MAGIC_TWO') & 0xff,
        GZIPConstants.get('GZIP_COMPRESSION_METHOD_DEFLATE') & 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03])
    

