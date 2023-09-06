import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants


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

    def is_alligned_at_EOF(self, skipped):
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
            # GZIPHeader
