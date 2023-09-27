import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp
from formats.http.HttpConstants import HttpConstants


class ValuePostCRParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # CR not followed by LF ---> go back to the state you are coming from
            return header_parser.value_pre_cr_state

        if byte == HttpConstants.get('CR'):  # another CR ---> ignore
            return header_parser.value_post_cr_state
        if byte == HttpConstants.get('LF'):  # found LF --> end of line
            return header_parser.line_start_state

        header_parser.add_value_byte(byte)  # add the found byte: we are still parsing the value
        return header_parser.value_state
