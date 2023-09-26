import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp
from formats.http.HttpConstants import HttpConstants


class ValuePostLWSPParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # we have already added space ---> skip!
            return header_parser.value_post_lwsp_state

        if byte == HttpConstants.get('CR'):  # found CR
            header_parser.value_pre_cr_state = self
            return header_parser.value_post_cr_state
        if byte == HttpConstants.get('LF'):  # found LF --> end of line
            return header_parser.line_start_state

        header_parser.add_value_byte(byte)  # continue to parse rest of value bytes
        return header_parser.value_state
