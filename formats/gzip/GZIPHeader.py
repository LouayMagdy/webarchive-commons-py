import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPStaticHeader import GZIPStaticHeader
from formats.gzip.GZIPFExtraRecords import GZIPFExtraRecords
from formats.gzip.GZIPFExtraRecord import GZIPFExtraRecord
from utils.ByteOp import *


class GZIPHeader:
    def __init__(self, gzip_static_header: GZIPStaticHeader = None):
        self.static_header = GZIPStaticHeader() if gzip_static_header is None else gzip_static_header
        self.gzip_records = None
        self.filename = None
        self.filename_length = 0
        self.comment = None
        self.comment_length = 0
        self.crc = -1

    def get_static_header(self) -> GZIPStaticHeader:
        return self.static_header

    def get_file_name(self) -> bytearray:
        return self.filename

    def get_comment(self) -> bytearray:
        return self.comment

    def get_file_name_length(self) -> int:
        return self.filename_length

    def get_header_crc(self) -> int:
        return self.crc

    def get_comment_length(self) -> int:
        return self.comment_length

    def set_file_name(self, file_name: bytearray):
        if file_name is not None:
            self.filename = copy(file_name)
            self.static_header.set_fname_flag(True)
            self.filename_length = len(file_name)
        else:
            self.filename = None
            self.static_header.set_fname_flag(False)
            self.filename_length = 0
        self.crc = -1

    def set_file_comment(self, comment: bytearray):
        if comment is not None:
            self.comment = copy(comment)
            self.static_header.set_fcomment_flag(True)
            self.comment_length = len(comment)
        else:
            self.comment = None
            self.static_header.set_fcomment_flag(False)
            self.comment_length = 0
        self.crc = -1

    def replace_record(self, name: bytearray, value: bytearray):
        if self.gzip_records is not None:
            self.remove_all_records(name)
        self.add_record(name=name, value=value)

    def remove_all_records(self, name: bytearray):
        removed = 0
        if self.gzip_records is not None:
            kept = 0
            to_remove = []
            for record in self.gzip_records.records:
                if record.matches_name(name=name):
                    to_remove.append(record)
                    removed += 1
                else:
                    kept += 1
            for record in to_remove:
                self.gzip_records.remove(record)
            if kept == 0:
                self.gzip_records = None
                self.static_header.set_fextra_flag(False)
        if removed > 0:
            self.crc = -1

    def add_record(self, name:bytearray, value:bytearray=None, int_val:int=None):
        if self.gzip_records is None:
            self.gzip_records = GZIPFExtraRecords()
        if value is None:
            self.gzip_records.append(GZIPFExtraRecord(name=name, int_val=int_val))
        else:
            self.gzip_records.append(GZIPFExtraRecord(name=name, value=int_val))
        self.static_header.set_fextra_flag(True)
        self.crc = -1

    def get_record(self, index: int):
        if self.gzip_records is None or self.gzip_records.is_empty():
            raise IndexError("Index out of bound exception")
        return self.gzip_records.get(index)

    def get_record_count(self) -> int:
        return 0 if self.gzip_records is None else self.gzip_records.size()

    def get_record_by_name(self, name: bytearray) -> GZIPFExtraRecord | None:
        if self.gzip_records is not None:
            for record in self.gzip_records.records:
                if record.matches_name(name):
                    return record
        return None

    def get_int_record_by_name(self, name: bytearray) -> int:
        record = self.get_record_by_name(name)
        if record is None:
            return -1
        return bytes_to_int(byte_arr=record.get_value())

    def get_length(self) -> int:
        size = self.static_header.get_length()
        size += self.gzip_records.get_byte_length if self.gzip_records is not None else 0
        size += self.filename_length
        size += self.comment_length
        size += 2 if self.static_header.is_fhcrc_set() else 0
        return size

    def write_bytes(self, output_stream):
        orig_output_stream = output_stream
        if self.static_header.is_fhcrc_set() and self.crc == -1:
            # CRC outputstream heree
