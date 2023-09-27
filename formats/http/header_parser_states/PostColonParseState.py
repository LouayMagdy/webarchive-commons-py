import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp
from formats.http.HttpConstants import HttpConstants


class PostColonParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # ignore more spaces till the value begins
            return header_parser.post_colon_state

        header_parser.set_value_start_idx()  # some other character found: reset to mark header's value beginning

        if byte == HttpConstants.get('CR'):  # found CR
            header_parser.value_pre_cr_state = header_parser.post_colon_state
            return header_parser.value_post_cr_state
        if byte == HttpConstants.get('LF'):  # end of line
            return header_parser.line_start_state

        header_parser.add_value_byte(byte)  # add the byte found to the value
        return header_parser.value_state  # another state: go and parse rest of value bytes
