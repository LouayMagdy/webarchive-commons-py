import logging
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.gzip.GZIPConstants import GZIPConstants

def add_logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls

@add_logger
class GZIPMemberSeries:
    var_map = {
        "STATE_DEFLATING": 0,
        "STATE_IOERROR": 1,
        "STATE_ALIGNED": 2,
        "STATE_SCANNING": 3,
        "STATE_START": 4,
        "state": 4,
        "streamContext": None,
        "decoder": None,
        "header": None,
        "BUF_SIZE": 4096,
        "stream": None,
        "currentMember": None,
        "currentMemberStartOffset": 0,
        "strict": False,
        "gotEOF": False,
        "gotIOError": False,
        "buffer[]": None,
        "singleByteRead[]": None,
        "bufferPos": 0,
        "bufferSize": 0,
        "offset": 0
    }

    def __init__(self, binary_stream, context="unknown", offset=0, strict=True):
        decoder =

