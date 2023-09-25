import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpConstants import HttpConstants


class HttpMessage:
    def __init__(self):
        self.version = HttpConstants.get("VERSION_0")
        self.bytes = -1
        self.is_corrupt = None

    def get_version(self) -> int:
        return self.version

    def get_version_string(self) -> str:
        if self.version == HttpConstants.get("VERSION_1"):
            return HttpConstants.get("VERSION_1_STATUS")
        elif self.version == HttpConstants.get("VERSION_9"):
            return HttpConstants.get("VERSION_9_STATUS")
        return HttpConstants.get("VERSION_0_STATUS")

    def get_length(self) -> int:
        return self.bytes

    def message_corrupt(self):
        self.is_corrupt = True

    def is_corrupt(self) -> bool:
        return self.is_corrupt
