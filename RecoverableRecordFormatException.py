class RecoverableRecordFormatException(IOError):
    def __init__(self, message: str = None):
        if message is not None:
            super().__init__(message)

# try:
#     # Some code that may raise an exception
#     raise IOError("An I/O error occurred")
# except Exception as e:
#     # Wrap the exception in a GZIPFormatException and re-raise
#     raise RecoverableRecordFormatException from e
#
# try:
#     # Some code that may raise an exception
#     raise IOError("An I/O error occurred")
# except Exception as e:
#     # Wrap the exception in a GZIPFormatException and re-raise
#     raise RecoverableRecordFormatException("RRF Exception") from e
#
#
# try:
#     # Some code that may raise an exception
#     raise IOError("An I/O error occurred")
# except Exception as e:
#     # Wrap the exception in a GZIPFormatException and re-raise
#     raise RecoverableRecordFormatException
