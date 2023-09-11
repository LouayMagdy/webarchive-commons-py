import zlib


class CustomInflater:
    def __init__(self, output_size: int = 1024):
        self._decompressor = zlib.decompressobj(wbits=-zlib.MAX_WBITS)
        self._written_bytes = 0
        self._read_bytes = 0
        self._data = None
        self._data_length = 0
        self._output_size = output_size

    def set_input(self, data: bytearray):
        self._data = data
        self._data_length = len(data)
        self._read_bytes = 0
        self._written_bytes = 0

    def set_output_size(self, output_size):
        self._output_size = min(output_size, 1024)

    def inflate(self, output: bytearray) -> int:
        output[:] = self._decompressor.decompress(self._data, self._output_size)
        self._written_bytes += len(output)
        self._read_bytes = self._data_length - len(self._decompressor.unconsumed_tail)
        self._data = self._decompressor.unconsumed_tail
        return len(output)

    def get_bytes_written(self):
        return self._written_bytes

    def get_bytes_read(self):
        return self._read_bytes
