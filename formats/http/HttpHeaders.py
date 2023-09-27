import sys
import os
import logging
from datetime import datetime

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpHeaderObserver import HttpHeaderObserver
from formats.http.HttpHeader import HttpHeader
from formats.http.HttpConstants import HttpConstants
from utils.DateUtils import *
from utils.ByteOp import copy


def add_logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls


@add_logger
class HttpHeaders(HttpHeaderObserver):
    def __init__(self):
        self.is_corrupt = False
        self.total_bytes = 0
        self._headers = []

    def set_date_header(self, name: str, ms: int = None, date: datetime = None):
        if not date:
            self.set_date_header(name=name, date=datetime.fromtimestamp(ms/1000))
        else:
            self.set(name, get_rfc1123_date(date))

    def add_date_header(self, name: str, ms: int = None, date: datetime = None):
        if not date:
            self.add_date_header(name=name, date=datetime.fromtimestamp(ms / 1000))
        else:
            self.add(name, get_rfc1123_date(date=date))

    def get(self, name: str) -> HttpHeader | None:
        for header in self._headers:
            if header.get_name() == name:
                return header
        return None

    def get_value(self, name: str) -> str | None:
        header = self.get(name)
        return None if header is None else header.get_value()

    def get_value_case_insensitive(self, name: str) -> str | None:
        name_lower_case = name.lower()
        for header in self._headers:
            if header.get_name().lower() == name_lower_case:
                return header.get_value()
        return None

    def get_content_length(self):
        value_string = self.get_value_case_insensitive("content-length")
        if value_string:
            try:
                return int(value_string)
            except ValueError as e:
                self._logger.warning(e.args[0])
        return -1

    def to_string(self) -> str:
        result = "HttpHeaders:\n==========\n"
        for header in self._headers:
            result += f"\t{header.to_string()}\n"
        return result + "========\n"

    def header_parsed(self, name: bytearray, name_start: int, name_length: int, value: bytearray, value_start: int,
                      value_length: int):
        s_name = copy(name, 0, name_length).decode(HttpConstants.get('UTF8'))
        s_value = copy(value, 0, value_length).decode(HttpConstants.get('UTF8'))
        self.add(s_name, s_value)

    def headers_complete(self, total_bytes: int):
        self.total_bytes = total_bytes

    def headers_corrupt(self) -> bool:
        return self.is_corrupt

    def get_total_bytes(self) -> int:
        return self.total_bytes

    def set(self, name: str, value: str):
        header = self.get(name)
        if header:
            header.set_value(value)
        else:
            self.add(name, value)

    def add(self, name: str, value: str):
        self._headers.append(HttpHeader(name, value))

    def write(self, output_stream):
        for header in self._headers:
            header.write(output_stream)
        output_stream.write(bytearray([HttpConstants.get('CR')]))
        output_stream.write(bytearray([HttpConstants.get('LF')]))


# headers = HttpHeaders()
# headers.add("Accept-Language", "en-US,en;q=0.5")
# headers.add("Authorization", "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==")
# headers.add("Content-Type", "application/json")
# headers.add("Cache-Control", "max-age=3600")
# print(headers.to_string())
# headers.set("Cache-Control", "max-age=4000")
# headers.set_date_header("at", date=datetime.datetime.now())
# print(headers.to_string())
# print(headers.get_content_length())
# print(headers.get_value('AT'), headers.get_value_case_insensitive('AT'))
#
# with open("./experimental/headers.txt", 'wb') as f_o:
#     headers.write(f_o)
