import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp, is_legal_name_byte
from formats.http.HttpParseException import HttpParseException
from formats.http.HttpConstants import HttpConstants


class LineStartParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # found space after LF --> add it + value still not ended
            header_parser.add_value_byte(HttpConstants.get('SP'))
            return header_parser.value_post_lwsp_state

        if is_legal_name_byte(byte):  # this must be the start of a new header
            header_parser.header_finished()
            header_parser.set_name_start_pos()
            header_parser.add_name_byte(byte)
            return header_parser.name_state

        if byte == HttpConstants.get('CR'):
            return header_parser.post_blank_cr_state

        if byte == HttpConstants.get('LF'):  # found LF ---> end of parsing headers
            header_parser.header_finished()
            header_parser.parse_finished()
            return header_parser.end_state

        if header_parser.is_strict():  # illegal character
            raise HttpParseException("Bad character at start of line")
        header_parser.headers_corrupted()
        return header_parser.lax_line_eat_parse_state





