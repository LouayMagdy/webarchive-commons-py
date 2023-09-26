import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp
from formats.http.HttpParseException import HttpParseException
from formats.http.HttpConstants import HttpConstants


class PostNameParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # ignore more spaces till u find the COLON
            return header_parser.post_name_state

        if byte == HttpConstants.get('COLON'):  # got COLON --> look where the header value starts
            return header_parser.post_colon_state

        if header_parser.is_strict():  # illegal character
            raise HttpParseException(f'Illegal char after name({header_parser.name[:header_parser.name_length]})')
        header_parser.headers_corrupted()
        return header_parser.lax_line_eat_parse_state
