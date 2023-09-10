class SimpleIS:

    def __init__(self, f_i):
        self.input_stream = f_i

    def read(self, buffer: bytearray=None, offset: int=0, length: int=None):
        if buffer is not None:
            if len(buffer) - offset < length:
                raise IndexError("Index out of bound error")
            buffer[offset:] = bytearray(self.input_stream.read(length))
            return len(buffer) if len(buffer) > 0 else -1
        elif length is not None:
            return bytearray(self.input_stream.read(length))
        else:
            return self.input_stream.read(1)

    def tell(self) -> int:
        return self.input_stream.tell()

    def seek(self, pos: int):
        self.input_stream.seek(pos)

    def fileno(self):
        return self.input_stream.fileno()