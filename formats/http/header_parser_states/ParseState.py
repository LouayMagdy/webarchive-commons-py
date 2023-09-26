from abc import ABC, abstractmethod
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from formats.http.HttpConstants import HttpConstants


class ParseState(ABC):
    @abstractmethod
    def handle_byte(self, byte, header_parser) -> 'ParseState':
        pass


def is_lwsp(byte) -> bool:
    return byte == HttpConstants.get('SP') or byte == HttpConstants.get('HTAB')


def is_legal_name_byte(byte) -> bool:
    if 31 < byte < 128:
        return byte != HttpConstants.get('SP') and byte != HttpConstants.get('COLON')
    return False
