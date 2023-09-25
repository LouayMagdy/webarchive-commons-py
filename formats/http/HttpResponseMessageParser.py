import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpMessageParser import HttpMessageParser
from formats.http.HttpResponseMessage import HttpResponseMessage
from formats.http.HttpResponseMessageObserver import HttpResponseMessageObserver


class HttpResponseMessageParser(HttpMessageParser):
    def __init__(self) -> None:
        super().__init__()
        max_bytes = 1024 * 128
        strict = False

    def parse_message(self, input_stream) -> HttpResponseMessage:
        message = HttpResponseMessage()
        self.parse(input_stream, message)
        return message

    def parse(self, obs: HttpResponseMessageObserver, input_stream = None, buffer: bytearray = None, len: int = None):


