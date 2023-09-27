import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpConstants import HttpConstants
from formats.http.HttpParseException import HttpParseException


class HttpMessageParser:
    def parse_version_strict(self, buffer: bytearray, start: int, length: int) -> int:
        v = buffer[start: start + length].decode(HttpConstants.get("UTF8"))
        if v == HttpConstants.get("VERSION_0_STATUS"):
            return HttpConstants.get("VERSION_0")
        elif v == HttpConstants.get("VERSION_1_STATUS"):
            return HttpConstants.get("VERSION_1")
        elif v == HttpConstants.get("VERSION_9_STATUS"):
            return HttpConstants.get("VERSION_9")
        else:
            raise HttpParseException("Unknown version")

    def parse_version_lax(self, buffer: bytearray, start: int, length: int) -> int:
        v = buffer[start: start + length].decode(HttpConstants.get("UTF8")).lower()
        if v == HttpConstants.get("VERSION_1_STATUS").lower():
            return HttpConstants.get("VERSION_1")
        elif v == HttpConstants.get("VERSION_9_STATUS").lower():
            return HttpConstants.get("VERSION_9")
        else:
            return HttpConstants.get("VERSION_0")

