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

    def inflate(self, output: bytearray, offset: int = 0, length: int = None) -> int:
        if length is None:
            length = len(output)
        if length + offset > len(output):
            raise IndexError("Index out of Bound")
        temp_out = self._decompressor.decompress(self._data, min(self._output_size, length))
        output[offset: offset + len(temp_out)] = temp_out[:]
        self._written_bytes += len(temp_out)
        self._read_bytes = self._data_length - len(self._decompressor.unconsumed_tail)
        self._data = self._decompressor.unconsumed_tail
        return len(temp_out)

    def get_bytes_written(self) -> int:
        return self._written_bytes

    def get_bytes_read(self) -> int:
        return self._read_bytes

    def needs_input(self) -> bool:
        return self._data_length == self._read_bytes

    def finished(self) -> bool:
        return self._decompressor.eof

    def get_remaining(self):
        return self._decompressor.unconsumed_tail
