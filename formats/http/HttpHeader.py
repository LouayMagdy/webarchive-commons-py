import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpConstants import HttpConstants


class HttpHeader:
    def __init__(self, name: str = None, value: str = None):
        self._name = name
        self._value = value

    def get_name(self) -> str:
        return self._name

    def get_value(self) -> str:
        return self._value

    def set_name(self, name: str):
        self._name = name

    def set_value(self, value: str):
        self._value = value

    def write(self, output_stream):
        output_stream.write(self._name.encode(HttpConstants.get('UTF8')))
        output_stream.write(bytearray([HttpConstants.get('COLON')]))
        output_stream.write(bytearray([HttpConstants.get('SP')]))
        output_stream.write(self._value.encode(HttpConstants.get('UTF8')))
        output_stream.write(bytearray([HttpConstants.get('CR')]))
        output_stream.write(bytearray([HttpConstants.get('LF')]))

    def to_string(self) -> str:
        return f"HttpHeader({self._name})({self._value})"
