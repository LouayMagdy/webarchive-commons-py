import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPStaticHeader import GZIPStaticHeader
from formats.gzip.GZIPFExtraRecords import GZIPFExtraRecords
from formats.gzip.GZIPFExtraRecord import GZIPFExtraRecord
from utils.ByteOp import *
from utils.io.CRCOutputStream import CRCOutputStream


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

    def add_record(self, name: bytearray, value: bytearray = None, int_val: int = None):
        if self.gzip_records is None:
            self.gzip_records = GZIPFExtraRecords()
        if value is None:
            self.gzip_records.add(GZIPFExtraRecord(name=name, int_val=int_val))
        else:
            self.gzip_records.add(GZIPFExtraRecord(name=name, value=value))
        self.static_header.set_fextra_flag(True)
        self.crc = -1

    def get_record(self, index: int) -> GZIPFExtraRecord:
        if self.gzip_records is None or self.gzip_records.is_empty() or index >= self.get_record_count():
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
            output_stream = CRCOutputStream(orig_output_stream)
        self.static_header.write_to(output_stream=output_stream)
        if self.static_header.is_fextra_set():
            self.gzip_records.write_to(output_stream=output_stream)
        if self.static_header.is_fname_set():
            output_stream.write_byte_arr(self.filename)
        if self.static_header.is_fcomment_set():
            output_stream.write_byte_arr(self.comment)
        if self.static_header.is_fhcrc_set():
            if self.crc == -1:
                self.crc = output_stream.get_crc_value()
            write_short(short_val=self.crc, output_stream=orig_output_stream)

    @staticmethod
    def is_valid_compression_method(cm: int) -> bool:
        return cm == GZIPConstants.get("GZIP_COMPRESSION_METHOD_DEFLATE")

# gzsh = GZIPStaticHeader() gzh = GZIPHeader(gzip_static_header=gzsh) gzh.set_file_name(bytearray("Louay",
# 'utf-8')) print(gzh.get_file_name(), gzh.get_file_name_length()) gzh.set_file_comment(bytearray("this is the 1st
# trial", 'utf-8')) print(gzh.get_comment(), gzh.get_comment_length()) gzh.add_record(name=bytearray('f1', 'utf-8'),
# int_val=456) gzh.add_record(name=bytearray('f2', 'utf-8'), value=bytearray([14, 23, 69, 64, 58])) gzh.add_record(
# name=bytearray('f1', 'utf-8'), value=bytearray([14, 64, 58])) print(gzh.get_int_record_by_name(bytearray('f1',
# 'utf-8'))) print(gzh.get_int_record_by_name(bytearray('f2', 'utf-8')), bytes_to_int(byte_arr=bytearray([14, 23, 69,
# 64, 58]), offset=0)) print(f"count:{gzh.get_record_count()}") gzh.replace_record(name=bytearray('f1', 'utf-8'),
# value=bytearray([12, 13])) print(gzh.get_record_count()) print(gzh.get_record_by_name(bytearray('f1',
# 'utf-8')).get_value())
