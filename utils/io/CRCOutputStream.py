

class CRCOutputStream:
    "this class is supposed to extend Outputstream so, extra methods are found as tell and seek"

    def __init__(self, output_stream, auto_flush: bool = False):
        self.output_stream = output_stream
        # self._crc_32
        self.auto_flush = auto_flush
        self.bytes_written = 0

    
