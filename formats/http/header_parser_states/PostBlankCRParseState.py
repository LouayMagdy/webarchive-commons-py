import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState
from formats.http.HttpParseException import HttpParseException
from formats.http.HttpConstants import HttpConstants


class PostBlankCRParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if byte == HttpConstants.get('LF'):  # LF CR LF  ---> end of all headers
            header_parser.header_finished()
            header_parser.parse_finished()
            return header_parser.end_state

        if header_parser.is_strict():
            raise HttpParseException("NON LF after blank CR")
        header_parser.headers_corrupted()
        return header_parser.lax_line_eat_parse_state
