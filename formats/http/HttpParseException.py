from RecoverableRecordFormatException import RecoverableRecordFormatException


class HttpParseException(RecoverableRecordFormatException):
    def __init__(self, message: str = None):
        super().__init__(message)
