import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPFormatException import GZIPFormatException, GZIPExtraFieldShortException
from formats.gzip.GZIPFExtraRecord import GZIPFExtraRecord
from utils.ByteOp import *


class GZIPFExtraRecords:
    def __init__(self, input_stream=None):
        self.records = []
        if input_stream is not None:
            self.read_records(input_stream)

    def write_to(self, output_stream):
        over_all_len = 0
        for record in self.records:
            over_all_len += record.length()
        write_short(short_val=over_all_len, output_stream=output_stream)
        for record in self.records:
            record.write_to(output_stream=output_stream)

    def get_byte_length(self) -> int:
        length = 2
        # the length of all records is written in 2 bytes
        for record in self.records:
            length += record.length()
        return length

    def read_records(self, input_stream):
        self.records = []
        remaining_bytes = -1
        remaining_bytes = read_short(input_stream=input_stream)
        if remaining_bytes < 0:
            raise GZIPFormatException("Negative FExtra length")
        tmp_list = []
        while remaining_bytes:
            tmp_record = GZIPFExtraRecord()
            try:
                read_bytes = tmp_record.read(input_stream=input_stream, max_to_read=remaining_bytes)
                remaining_bytes -= read_bytes
                tmp_list.append(tmp_record)
            except GZIPExtraFieldShortException as ex:
                remaining_bytes -= ex.bytes_read
            if remaining_bytes < 0:
                raise GZIPFormatException("Invalid FExtra length/records")
        self.records = tmp_list

    "----> the next methods are list methods to deal with this class"

    def add(self, record: GZIPFExtraRecord):
        self.records.append(record)

    def remove(self, record: GZIPFExtraRecord):
        self.records.remove(record)

    def get(self, index: int) -> GZIPFExtraRecord:
        return self.records[index]

    def is_empty(self) -> bool:
        return len(self.records) == 0

    def size(self) -> int:
        return len(self.records)

# t1 = GZIPFExtraRecord(name=bytearray([23, 34]), value=bytearray([12, 56, 39]))
# t2 = GZIPFExtraRecord(name=bytearray([13, 84]), value=bytearray([10, 97, 65, 93]))
# t3 = GZIPFExtraRecord(name=bytearray([67, 51]), value=bytearray([14, 63, 48, 49, 52]))
# print(t1.get_name(), t1.get_value())
# print(t2.get_name(), t2.get_value())
# print(t3.get_name(), t3.get_value())
# with open('./experimental/writing_short.txt', 'ab') as f_o:
#     write_short(short_val=24, output_stream=f_o)
#     t1.write_to(f_o)
#     t2.write_to(f_o)
#     t3.write_to(f_o)
# records = None
# with open("./experimental/writing_short.txt", 'rb') as f_i:
#     records = GZIPFExtraRecords(input_stream=f_i)
#     for record in records.records:
#         print(record.get_name(), record.get_value())
#     print(records.get_byte_length())
# with open("./experimental/writing_short.txt", 'wb') as f_o:
#     records.write_to(output_stream=f_o)
