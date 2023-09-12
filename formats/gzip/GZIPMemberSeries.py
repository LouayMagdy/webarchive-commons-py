import logging
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPDecoder import GZIPDecoder
from formats.gzip.GZIPFormatException import *
from formats.gzip.GZIPSeriesMember import GZIPSeriesMember
from streamcontext.Stream import Stream
from utils.CustomInflater import CustomInflater


def add_logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls


@add_logger
class GZIPMemberSeries:
    constants = {
        "STATE_DEFLATING": 0,  # a gzip header and some amount of deflate information has been read, without errors
        "STATE_IOERROR": 1,  # an IOException has been detected on the underlying Stream
        "STATE_ALIGNED": 2,  # the gzip footer of a record has *just* been read, and it is expected that the underlying
                             # Stream is either at EOF, or at the start of another gzip member.
                             # In Strict Mode this is the initial state.
        "STATE_SCANNING": 3,  # The underlying Stream is in an unknown state - either because of a GZ error in the
                              # previous member, and we're now attempting to locate the next member.
                              # In Lax Mode, this is the initial state.
        "STATE_START": 4,
        "BUF_SIZE": 4096,
    }

    def __init__(self, binary_stream: Stream, context="unknown", offset=0, strict=True):
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
            raise IOError(
                f"note_end_of_record while not deflating at {self._current_member_start_offset} in {self._stream_context}")
        self.state = self.constants.get('STATE_ALIGNED')

    def note_gz_error(self):
        self._logger.info("noteGZError")
        if self._strict:
            self._got_io_error = True
            self.state = self.constants.get("STATE_IOERROR")
            curr_mem_start_offset, context = self._current_member_start_offset, self._stream_context
            raise IOError(f"Internal GZIPFormatException {curr_mem_start_offset} in {context}")
        self.state = self.constants.get('STATE_SCANNING')

    def get_next_member(self) -> GZIPSeriesMember | None:
        if self.state == self.constants.get('STATE_IOERROR'):
            curr_mem_start_offset, context = self._current_member_start_offset, self._stream_context
            raise IOError(f"get_next_member on IOError Stream at {curr_mem_start_offset} in {context}")
        self._logger.info("get_next_member")
        if self._got_eof:
            self._logger.info("get_next_member AT EOF")
            return None
        if self.state == self.constants.get('STATE_DEFLATING'):
            self._logger.info("get_next_member - without complete read -> finishing current")
            try:
                self._current_member.skip_member()
                self._logger.info("Skipped unfinished member")
            except GZIPFormatException as e:
                self._logger.info("GZIPFormatException on skip_member()")
                if self._strict:
                    raise GZIPFormatException(f"GZIPFormatException at {self._offset} in {self._stream_context}")
                # state now is STATE_SCANNING
        elif self.state == self.constants.get('STATE_SCANNING'):
            # gzip error with the prev. record: move the underlying Stream back to 3 bytes after the last member start
            curr_mem_start_offset_p3 = self._current_member_start_offset + 3
            self._logger.warning(f"getNextMember() called when scanning - starting from {curr_mem_start_offset_p3}")
            self._offset, self._buffer_size, self._buffer_pos = curr_mem_start_offset_p3, 0, 0
            self._stream.set_offset(curr_mem_start_offset_p3)

        self._current_member = None
        while not self._current_member:
            # scan the next record - note that this class is extending input stream
            amount_skipped = self._decoder.align_on_magic3(self)
            if self._logger.isEnabledFor(logging.INFO):
                self._logger.info(f"AlignedResult:{amount_skipped}")
            if amount_skipped < 0:
                # it reaches EOF without finding any magic bytes
                self._got_eof = True
                if self._decoder.is_aligned_at_eof(amount_skipped):
                    self._logger.info("CleanEOF")
                else:
                    if self._strict:
                        raise GZIPFormatException(f"Trailing bytes did not contain a valid gzip member "
                                                  f"file:{self._stream_context} offset: {self._current_member_start_offset}")
                    if self._logger.isEnabledFor(logging.INFO):
                        self._logger.info(
                            f"Got EOF after {-amount_skipped} bytes before finding magic in {self._stream_context}\n")
                return None
            if amount_skipped > 0:
                if self._strict:
                    if self.state == self.constants.get('STATE_START'):
                        self._logger.info(f"Strict mode Skipped {amount_skipped} bytes in {self._stream_context}"
                                          f" before finding magic at offset {self._offset - 3}\n")
                    else:
                        raise GZIPFormatException(
                            f"Not aligned at gzip start: {self._stream_context} at offset {self._offset - 3}")
                if self._logger.isEnabledFor(logging.INFO):
                    self._logger.info(
                        f"Skipped {amount_skipped} bytes in {self._stream_context} before finding magic at offset{self._offset - 3}\n")
            try:
                self._current_member_start_offset = self._offset - 3
                self._header = self.decoder.parse_header(orig_input_stream=self, assume1st3=True)
                self._logger.info("Read next GZip header...")
                self._current_member = GZIPSeriesMember(self, self._header)
                self.state = self.constants.get('STATE_DEFLATING')
            except GZIPFormatException as e:
                if self._strict:
                    self._got_io_error = True
                    raise IOError(f"{e} at {self._offset} in {self._stream_context}")
                self._offset = self._current_member_start_offset + 3
                self._stream.set_offset(self._current_member_start_offset + 3)
                self._logger.warning(
                    f"GZIPFormatException with record around offset {self._offset} in {self._stream_context}\n")
        return self._current_member

    # the next method is because this class is extending input stream
    def read(self, b: bytearray = None, offset: int = 0, length: int = None):
        if b is None:
            amt = self.read(self._single_byte_read, 0, 1)
            return -1 if amt == -1 else self._single_byte_read[0] & 0xFF
        else:
            if length is None:
                length = len(b)
            amt_written = 0
            if self._logger.isEnabledFor(logging.INFO):
                self._logger.info(f'read({length} bytes) bufferSize({self._buffer_size})')
            while length > 0:
                if self._buffer_size > 0:
                    amt_to_copy = min(length, self._buffer_size)
                    b[offset: offset + amt_to_copy] = self._buffer[self._buffer_pos: self._buffer_pos + amt_to_copy]
                    self._buffer_pos += amt_to_copy
                    self._buffer_size -= amt_to_copy
                    offset += amt_to_copy
                    length -= amt_to_copy
                    amt_written += amt_to_copy
                    self._offset += amt_to_copy
                elif not self.fill_buffer():
                    break
            return -1 if amt_written == 0 else amt_written

    def fill_buffer(self) -> bool:
        try:
            amt_read = self._stream.read(self._buffer, 0, len(self._buffer))
            if self._logger.isEnabledFor(logging.INFO):
                self._logger.info(f"Underlying Stream read({amt_read}) bytes")
            if amt_read == -1:
                self._got_eof = True
                return False
            self._buffer_pos = 0
            self._buffer_size += amt_read
        except IOError as e:
            self._got_io_error = True
            raise e
        return True

    def return_bytes(self, bytes_int: int):
        if bytes_int > self._buffer_pos or bytes_int < 0:
            raise IndexError("Index Out of Bound Error")
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(f"Returned ({bytes_int})bytes")
        self._buffer_pos -= bytes_int
        self._buffer_size += bytes_int
        self._offset -= bytes_int

    def fill_inflater(self, inflater: CustomInflater) -> int:
        if self.state != self.constants.get('STATE_DEFLATING'):
            raise IOError("fill_inflater() called while not deflating!")
        if self._buffer_size <= 0 and not self.fill_buffer():
            return -1
        inflater.set_input(data=self._buffer, offset=self._buffer_pos, length=self._buffer_size)
        self._buffer_pos += self._buffer_size
        self._offset += self._buffer_size
        old_size = self._buffer_size
        self._buffer_size = 0
        return old_size

    def is_strict(self) -> bool:
        return self._strict

    def set_strict(self, strict: bool):
        self._strict = strict
