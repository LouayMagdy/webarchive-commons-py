import sys
import os
import json
import logging

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPSeriesMember import GZIPSeriesMember
from my_resource.MetaData import MetaData
from my_resource.ResourceConstants import ResourceConstants
from utils.ByteOp import *


def add_logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls


@add_logger
class GZIPMetaData(MetaData):
    def __init__(self, parent_meta_data: MetaData):
        super().__init__(parent_meta_data, ResourceConstants.get('GZIP'))

    def set_data(self, gzip_member: GZIPSeriesMember):
        try:
            header = gzip_member.get_header()
            static_header = header.get_static_header()
            if static_header.is_fname_set():
                self.put(ResourceConstants.get('GZIP_FILENAME'), header.get_file_name().decode('utf-8'))
            if static_header.is_fcomment_set():
                self.put(ResourceConstants.get('GZIP_COMMENT_LENGTH'), header.get_comment_length())
            if static_header.is_fhcrc_set():
                self.put(ResourceConstants.get('GZIP_HEADER_CRC'), header.get_header_crc())
            record_count = header.get_record_count()
            for i in range(record_count):
                record, rec_dict = header.get_record(i), {}
                name = record.get_name().decode('utf-8')
                rec_dict[ResourceConstants.get('GZIP_FEXTRA_NAME')] = name
                if name == "SL" or name == "LX":
                    rec_dict[ResourceConstants.get('GZIP_FEXTRA_VALUE')] = bytes_to_int(byte_arr=record.get_value())
                else:
                    rec_dict[ResourceConstants.get('GZIP_FEXTRA_VALUE')] = draw_hex(byte_arr=record.get_value())
                self.append_child(ResourceConstants.get('GZIP_FEXTRA'), json.dumps(rec_dict))
            self.put(ResourceConstants.get('GZIP_DEFLATE_LENGTH'), gzip_member.get_compressed_bytes_read())
            self.put(ResourceConstants.get('GZIP_HEADER_LENGTH'), header.get_length())
            self.put(ResourceConstants.get('GZIP_FOOTER_LENGTH'), GZIPConstants.get('GZIP_FOOTER_BYTES'))
            footer = gzip_member.get_footer()
            self.put(ResourceConstants.get('GZIP_INFLATED_CRC'), footer.get_crc())
            self.put(ResourceConstants.get('GZIP_INFLATED_LENGTH'), footer.get_length())
        except (UnicodeError, LookupError, TypeError) as e:
            self._logger.warning(e.args[0])
