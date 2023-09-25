import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpMessage import HttpMessage
from formats.http.HttpResponseMessageObserver import HttpResponseMessageObserver
from formats.http.HttpConstants import HttpConstants


class HttpResponseMessage(HttpMessage, HttpResponseMessageObserver):

    def __init__(self, version: int = None, status: int = 0, reason: str = None):
        super().__init__()
        self.status = status
        self.reason = reason
        if version:
            self.version = version

    def get_status(self) -> int:
        return self.status

    def get_reason(self) -> str:
        return self.reason

    def to_string(self) -> str:
        return f"{self.get_version_string()} {self.status} {self.reason}{HttpConstants.get('CRLF')}"

    def to_debug_string(self) -> str:
        return f"Message({len(self.reason)}):({self.get_version_string()}) ({self.status}) ({self.reason}){HttpConstants.get('CRLF')}\n"

    def message_parsed(self, version: int, status: int, reason: str, bytes: int):
        self.version = version
        self.status = status
        self.reason = reason
        self.bytes = bytes
