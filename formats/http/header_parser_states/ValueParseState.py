import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.header_parser_states.ParseState import ParseState, is_lwsp
from formats.http.HttpConstants import HttpConstants


class ValueParseState(ParseState):
    def handle_byte(self, byte, header_parser) -> ParseState:
        if is_lwsp(byte):  # found space in parsing value ---> add the space, continue till CR LF
            header_parser.add_value_byte(HttpConstants.get('SP'))
            return header_parser.value_post_lwsp_state

        if byte == HttpConstants.get('CR'):  # found CR
            header_parser.value_pre_cr_state = self
            return header_parser.value_post_cr_state
        if byte == HttpConstants.get('LF'):  # found LF --> end of line
            return header_parser.line_start_state

        header_parser.add_value_byte(byte)  # add the byte as a value byte
        return self
