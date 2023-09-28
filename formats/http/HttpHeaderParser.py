import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpHeaderObserver import HttpHeaderObserver
from formats.http.HttpConstants import HttpConstants
from formats.http.HttpHeaders import HttpHeaders
from formats.http.HttpParseException import HttpParseException
from formats.http.header_parser_states.EndParseState import EndParseState
from formats.http.header_parser_states.LAXLineEatParseState import LAXLineEatParseState
from formats.http.header_parser_states.LineStartParseState import LineStartParseState
from formats.http.header_parser_states.NameParseState import NameParseState
from formats.http.header_parser_states.PostBlankCRParseState import PostBlankCRParseState
from formats.http.header_parser_states.PostColonParseState import PostColonParseState
from formats.http.header_parser_states.PostNameParseState import PostNameParseState
from formats.http.header_parser_states.StartParseState import StartParseState
from formats.http.header_parser_states.ValueParseState import ValueParseState
from formats.http.header_parser_states.ValuePostCRParseState import ValuePostCRParseState
from formats.http.header_parser_states.ValuePostLWSPParseState import ValuePostLWSPParseState

DEFAULT_MAX_NAME_LENGTH = 1024 * 100
DEFAULT_MAX_VALUE_LENGTH = 1024 * 1024 * 10


class HttpHeaderParser:

    def __init__(self, obs: HttpHeaderObserver = None, max_name: int = DEFAULT_MAX_NAME_LENGTH,
                 max_value: int = DEFAULT_MAX_VALUE_LENGTH):
        self.name = bytearray(max_name)
        self.value = bytearray(max_value)
        self._obs = obs
        self.is_strict = False
        self.name_start_idx = 0
        self.name_length = 0
        self.value_start_idx = 0
        self.value_length = 0
        self.buffer_idx = 0

        self.start_state = StartParseState()
        self.end_state = EndParseState()
        self.line_start_state = LineStartParseState()
        self.name_state = NameParseState()
        self.post_name_state = PostNameParseState()
        self.post_colon_state = PostColonParseState()
        self.value_state = ValueParseState()
        self.value_post_lwsp_state = ValuePostLWSPParseState()
        self.value_post_cr_state = ValuePostCRParseState()
        self.post_blank_cr_state = PostBlankCRParseState()
        self.lax_line_eat_parse_state = LAXLineEatParseState()
        self.value_pre_cr_state = None
        self.state = self.start_state

    def reset(self):
        self.state = self.start_state
        self.buffer_idx = 0
        self.name_start_idx = 0
        self.value_start_idx = 0
        self.name_length = 0
        self.value_length = 0

    def set_observer(self, obs: HttpHeaderObserver):
        self._obs = obs

    def is_strict(self) -> bool:
        return self.is_strict

    def parse_headers(self, input_stream):
        headers = HttpHeaders()
        self._obs = headers
        self.do_parse(input_stream)
        return headers

    def do_parse(self, input_stream, obs: HttpHeaderObserver = None):
        if obs:
            self._obs = obs
        bytes_read = 0
        self.reset()
        while not self.is_done():
            i = input_stream.read(1)
            if i == b'':
                if self.is_strict:
                    raise HttpParseException("EOF before CRLFCRLF")
                self.headers_corrupted()
                return bytes_read
            bytes_read += 1
            if i[0] > 127:
                if self.is_strict:
                    raise HttpParseException("Non ASCII byte in headers")
                self.headers_corrupted()
                continue
            self.parse_byte(i[0] & 0xFF)
        return bytes_read

    def is_done(self) -> bool:
        return isinstance(self.state, EndParseState)

    def parse_byte(self, b):
        self.state = self.state.handle_byte(byte=b, header_parser=self)
        self.buffer_idx += 1

    def header_finished(self):
        if not self.name_length:
            return
        if self.value_length > 0 and self.value[self.value_length - 1] == HttpConstants.get('SP'):
            self.value_length -= 1
        if self._obs:
            self._obs.header_parsed(self.name, self.name_start_idx, self.name_length,
                                    self.value, self.value_start_idx, self.value_length)

    def parse_finished(self):
        if self._obs:
            self._obs.headers_complete(self.buffer_idx + 1)

    def headers_corrupted(self):
        if self._obs:
            self._obs.headers_corrupt()

    def set_name_start_pos(self):
        self.name_start_idx = self.buffer_idx
        self.name_length = 0

    def add_name_byte(self, b):
        if self.name_length > len(self.name):
            raise HttpParseException("Name too long")
        self.name[self.name_length] = b
        self.name_length += 1

    def set_value_start_pos(self):
        self.value_start_idx = self.buffer_idx
        self.value_length = 0

    def add_value_byte(self, b):
        sp = HttpConstants.get('SP')
        if b == sp and (not self.value_length or self.value[self.value_length - 1] == sp):
            return
        if self.value_length > len(self.value):
            raise HttpParseException("Value too long")
        self.value[self.value_length] = b
        self.value_length += 1





