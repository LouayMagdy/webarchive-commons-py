import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPHeader import GZIPHeader
from formats.gzip.GZIPStaticHeader import GZIPStaticHeader
from formats.gzip.GZIPFExtraRecords import GZIPFExtraRecords
from formats.gzip.GZIPFormatException import GZIPFormatException
from utils.io.CRCInputStream import CRCInputStream
from utils.CRC32 import CRC32
from utils.ByteOp import *


class GZIPDecoder:
    SEARCH_EOF_AT_START = -(sys.maxsize - 1)

    def __init__(self, max_name_size=1024, max_comment_size=None):
        "note that if only max_name_size is provided, both attributes are set to it"
        if max_comment_size is None:
            self._max_name_size = max_name_size
            self._max_comment_size = max_name_size
        else:
            self._max_name_size = max_name_size
            self._max_comment_size = max_comment_size

    def is_aligned_at_eof(self, skipped):
        return skipped == self.SEARCH_EOF_AT_START

    def align_on_magic3(self, input_stream):
        bytes_skipped = 0
        look_ahead = bytearray(3)
        keep = 0
        while 1:
            if keep == 2:
                look_ahead[0] = look_ahead[1]
                look_ahead[1] = look_ahead[2]
            elif keep == 1:
                look_ahead[0] = look_ahead[2]
            amt = input_stream.read(look_ahead, keep, 3 - keep)
            if amt == -1:
                skipped_before_eof = bytes_skipped + keep
                return self.SEARCH_EOF_AT_START if skipped_before_eof == 0 else -1 * skipped_before_eof

            if look_ahead[0] != GZIPConstants.get("GZIP_MAGIC_ONE"):
                if look_ahead[1] == GZIPConstants.get("GZIP_MAGIC_ONE") and look_ahead[2] == GZIPConstants.get(
                        "GZIP_MAGIC_TWO"):
                    keep = 2
                elif look_ahead[2] == GZIPConstants.get("GZIP_MAGIC_ONE"):
                    keep = 1
                else:
                    keep = 0
                bytes_skipped += (3 - keep)
                continue
            if (look_ahead[1] & 0xff) != GZIPConstants.get('GZIP_MAGIC_TWO'):
                if look_ahead[2] == GZIPConstants.get('GZIP_MAGIC_ONE'):
                    keep = 1
                else:
                    keep = 0
                bytes_skipped += (3 - keep)
                continue
            if not GZIPHeader.is_valid_compression_method(look_ahead[2]):
                if look_ahead[2] == GZIPConstants.get('GZIP_MAGIC_ONE'):
                    keep = 1
                bytes_skipped += (3 - keep)
                continue
            return bytes_skipped

    def parse_header(self, orig_input_stream, assume1st3: bool = False) -> GZIPHeader:
        header, crc_input_stream, static_header = None, None, None
        if assume1st3:
            crc = CRC32()
            crc.update(GZIPStaticHeader.DEFAULT_HEADER_DATA[:3])
            crc_input_stream = CRCInputStream(orig_input_stream, crc)
            static_header = GZIPStaticHeader(crc_input_stream, assume1st3=True)
        else:
            crc_input_stream = CRCInputStream(orig_input_stream)
            static_header = GZIPStaticHeader(crc_input_stream)
        header = GZIPHeader(static_header)
        if static_header.is_fextra_set():
            header.gzip_records = GZIPFExtraRecords(input_stream=crc_input_stream)
        if static_header.is_fname_set():
            if self._max_name_size > 0:
                header.filename = read_to_null(input_stream=crc_input_stream, max_size=self._max_name_size)
                header.filename_length = len(header.filename)
            else:
                header.filename = None
                header.filename_length = discard_to_null(crc_input_stream)
        if static_header.is_fcomment_set():
            if self._max_comment_size > 0:
                header.comment = read_to_null(input_stream=crc_input_stream, max_size=self._max_comment_size)
                header.comment_length = len(header.comment)
            else:
                header.comment = None
                header.comment_length = discard_to_null(crc_input_stream)
        if static_header.is_fhcrc_set():
            header.crc = read_short(input_stream=crc_input_stream)
            want_crc16 = crc_input_stream.get_crc_value() & 0xFFFF
            if want_crc16 != header.crc:
                raise GZIPFormatException("HEADER CRC ERROR")
        return header
