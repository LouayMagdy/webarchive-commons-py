import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp, is_legal_name_byte
from formats.http.HttpParseException import HttpParseException


class StartParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # spaces not allowed
            if header_parser.is_strict():
                raise HttpParseException("Space at start of headers")
            header_parser.headers_corrupted()
            return header_parser.start_state

        if is_legal_name_byte(byte):  # we should mark this as the beginning of the header name
            header_parser.set_name_start_pos()
            header_parser.add_name_byte(byte)
            return header_parser.name_state

        if header_parser.is_strict():  # we have found illegal character at the beginning of the name
            raise HttpParseException("Bad character at start of headers")
        header_parser.headers_corrupted()
        return header_parser.lax_line_eat_parse_state
