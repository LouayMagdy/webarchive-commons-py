import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState
from formats.http.HttpConstants import HttpConstants


class LAXLineEatParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if byte == HttpConstants.get('CR'):
            return header_parser.value_post_cr_state
        if byte == HttpConstants.get('LF'):
            return header_parser.line_start_state
        return header_parser.lax_line_eat_parse_state
