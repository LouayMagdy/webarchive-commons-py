import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp, is_legal_name_byte
from formats.http.HttpParseException import HttpParseException
from formats.http.HttpConstants import HttpConstants


class NameParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_legal_name_byte(byte):  # if we still get legal bytes --> add them to the name bytes
            header_parser.add_name_byte(byte)
            return self

        if is_lwsp(byte):  # got spaces --> ignore till u find COLON
            return header_parser.post_name_state
        if byte == HttpConstants.get('COLON'):  # got COLON --> look where the header value starts
            return header_parser.post_colon_state

        if header_parser.is_strict():  # illegal character
            raise HttpParseException("Illegal name char")
        header_parser.headers_corrupted()
        return header_parser.lax_line_eat_parse_state
