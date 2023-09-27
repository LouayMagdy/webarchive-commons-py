import logging
import os
import sys
import zlib
import threading

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPHeader import GZIPHeader
from formats.gzip.GZIPFooter import GZIPFooter
from formats.gzip.GZIPFormatException import *
from utils.CRC32 import CRC32
from utils.CustomInflater import CustomInflater

reset_lock = threading.Lock()


def add_logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls


@add_logger
class GZIPSeriesMember:
    SKIP_LENGTH = 1024 * 4

    def __init__(self, gzip_member_series, gzip_header: GZIPHeader):
        self._series = gzip_member_series
        self._header = gzip_header
        self._footer = None
        self._inflater = CustomInflater()
        self._crc = CRC32()
        self._got_io_error = False
        self._got_gz_error = False
        self._got_eor = False

    def get_footer(self) -> GZIPFooter:
        return self._footer

    def get_header(self) -> GZIPHeader:
        return self._header

    def get_record_start_offset(self) -> int:
        return self._series.get_current_member_start_offset()

    def get_record_file_context(self) -> str:
        return self._series.get_stream_context()

    def get_io_error(self) -> bool:
        return self._got_io_error

    def get_eor(self) -> bool:
        return self._got_eor

    def get_gz_error(self) -> bool:
        return self._got_gz_error

    def get_uncompressed_bytes_read(self) -> int:
        return self._inflater.get_bytes_written()

    def get_compressed_bytes_read(self) -> int:
        amount_read = self._header.get_length() + self._inflater.get_bytes_read()
        return amount_read + GZIPConstants.get("GZIP_STATIC_FOOTER_SIZE") if self._got_eor else amount_read

    def skip_member(self):
        self.skip(sys.maxsize)

    # the following methods are because this class is supposed to extend InputStream in the Java Code
    def read(self, b: bytearray = None, offset: int = 0, length: int = None) -> int:
        if b is not None:
            if length is None:
                length = len(b)
            total_read = 0
            if self._got_io_error:
                raise IOError("Repeated read() on IOException!")
            if self._got_gz_error:
                raise GZIPFormatException("Repeated read() on GZIPFormatException")
            if self._got_eor:
                return -1
            while total_read < length and not self._got_eor:
                if self._inflater.needs_input():
                    try:
                        amount_read = self._series.fill_inflater(self._inflater)
                    except IOError as e:
                        self._got_io_error = True
                        raise e
                    if amount_read == -1:
                        self._logger.warning('At end of file without inflate done...')
                        self._got_gz_error = True
                        raise GZIPFormatException("At end of file without inflate done...")

                try:
                    amount_inflated = self._inflater.inflate(output=b, offset=offset + total_read,
                                                             length=length - total_read)
                except zlib.error as e:
                    self._logger.warning("GOT GZ-ZLIBERROR")
                    self._got_gz_error = True
                    self._series.note_gz_error()
                    raise GZIPFormatException() from e

                finished = self._inflater.finished()
                self._crc.update(byte_arr=b, offset=offset + total_read, length=amount_inflated)
                total_read += amount_inflated
                if finished:
                    self._series.return_bytes(self._inflater.get_remaining())
                    footer_buffer = bytearray(GZIPConstants.get("GZIP_STATIC_FOOTER_SIZE"))
                    footer_bytes = self._series.read(footer_buffer, 0, len(footer_buffer))
                    if footer_bytes != GZIPConstants.get("GZIP_STATIC_FOOTER_SIZE"):
                        self._got_gz_error = True
                        self._series.note_gz_error()
                        raise GZIPFormatException("short footer")
                    self._got_eor = True
                    self._series.note_end_of_record()
                    try:
                        tmp_footer = GZIPFooter(buffer=footer_buffer)
                        tmp_footer.verify(self._crc.get_value(), self._inflater.get_bytes_written())
                        self._footer = tmp_footer
                    except GZIPFormatException as e:
                        self._got_gz_error = True
                        self._series.note_gz_error()
                        raise e
                    if total_read == 0:
                        total_read = -1
            return total_read
        else:
            buffer = bytearray(1)
            amt = self.read(b=buffer, offset=0, length=1)
            return -1 if amt == -1 else buffer[0] & 0xFF

    def available(self) -> int:
        return 0 if self._got_eor else int(not self._inflater.needs_input())

    def close(self):
        self.skip_member()

    def mark(self):
        return

    def mark_supported(self) -> bool:
        return False

    def reset(self):
        with reset_lock:
            raise IOError("reset() not supported")

    def skip(self, amt: int) -> int:
        skipped = 0
        b = bytearray(self.SKIP_LENGTH)
        while amt > 0:
            r = self.read(b, offset=0, length=len(b))
            if r == -1:
                break
            skipped += r
            amt -= r
        return skipped
