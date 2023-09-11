import logging
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPDecoder import GZIPDecoder
from formats.gzip.GZIPFormatException import *
from formats.gzip.GZIPSeriesMember import GZIPSeriesMember


def add_logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls


@add_logger
class GZIPMemberSeries:
    constants = {
        "STATE_DEFLATING": 0,
        "STATE_IOERROR": 1,
        "STATE_ALIGNED": 2,
        "STATE_SCANNING": 3,
        "STATE_START": 4,
        "BUF_SIZE": 4096,
    }

    def __init__(self, binary_stream, context="unknown", offset=0, strict=True):
        self._decoder = GZIPDecoder()
        self._stream = binary_stream
        self._strict = strict
        self.state = self.constants.get('STATE_ALIGNED') if strict and not offset else self.constants.get('STATE_START')
        self._buffer = bytearray(self.constants.get("BUF_SIZE"))
        self._single_byte_read = bytearray(1)
        self._current_member = None
        self._current_member_start_offset = 0
        self._got_eof = False
        self._got_io_error = False
        self._header = None
        self._stream_context = context
        self._offset = offset
        self._buffer_pos = 0
        self._buffer_size = 0

    def close(self):
        self._stream.close()
        self._got_eof = True

    def got_eof(self) -> bool:
        return self._got_eof

    def got_io_error(self) -> bool:
        return self._got_io_error

    def get_stream_context(self) -> str:
        return self._stream_context

    def get_current_member_start_offset(self) -> int:
        return self._current_member_start_offset

    def get_offset(self) -> int:
        return self._offset

    def note_end_of_record(self):
        if self.state != self.constants.get('STATE_DEFLATING'):
            self._got_io_error = True
            raise IOError(f"noteEndOfRecord while not deflating at {self._current_member_start_offset} in {self._stream_context}")
        self.state = self.constants.get('STATE_ALIGNED')

    def note_gz_error(self):
        self._logger.info("noteGZError")
        if self._strict:
            self._got_io_error = True
            self.state = self.constants.get("STATE_IOERROR")
            raise IOError(f"Internal GZIPFormatException {self._current_member_start_offset} in {self._stream_context}")
        self.state = self.constants.get('STATE_SCANNING')

    def get_next_member(self) -> GZIPSeriesMember:
        return GZIPSeriesMember()
