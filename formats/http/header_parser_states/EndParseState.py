import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState
from formats.http.HttpParseException import HttpParseException


class EndParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:  # No More Byte Handling
        raise HttpParseException('Parse already completed')
