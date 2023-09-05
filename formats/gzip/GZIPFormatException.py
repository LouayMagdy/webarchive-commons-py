import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from RecoverableRecordFormatException import RecoverableRecordFormatException


class GZIPFormatException(RecoverableRecordFormatException):
    def __init__(self, message: str = None):
        if message is not None:
            super().__init__(message)


class GZIPExtraFieldShortException(GZIPFormatException):
    def __init__(self, bytes_read: int):
        super().__init__("Extra Field short.")
        self.bytes_read = bytes_read

# see RecoverableRecordFormatException to understand how to use
