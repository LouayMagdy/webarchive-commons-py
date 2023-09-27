import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from utils.io.EOFObserver import EOFObserver


class EOFNotifyingInputStream:
    def __init__(self, input_stream, eof_observer: EOFObserver):
        self.input_stream = input_stream
        self.eof_observer = eof_observer
        self.notified = False

    def _do_notify(self):
        if not self.notified:
            self.notified = True
            if self.eof_observer:
                self.eof_observer.notify_eof()

    def read(self, b: bytearray = None, offset: int = 0, length: int = None):
        if b and length is None:
            length = len(b)
        amt_read = self.input_stream.read(b, offset, length)
        if amt_read == -1:
            self._do_notify()
        return amt_read
