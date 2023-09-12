import zlib
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from utils.CustomInflater import CustomInflater

read_count = 0

data = b"Hello there, Hello there, Hello there, Hello there, Hello there, "
compressor = zlib.compressobj(level=zlib.Z_BEST_COMPRESSION, wbits=-zlib.MAX_WBITS)
compressed_data = compressor.compress(data) + compressor.flush()
print(f"Compressed data: {compressed_data} of length = {len(compressed_data)}, {len(data)}")

l = 64
inflater = CustomInflater(l)
inflater.set_input(bytearray(compressed_data))
while 1:
    buffer = bytearray(l)
    size = inflater.inflate(buffer, 0, 1)
    if buffer == bytearray(l):
        break
    print(f"{buffer.decode()} --- bytes inflated: {size} --- read till now: {inflater.get_bytes_read()} --- written "
          f"till now: {inflater.get_bytes_written()}")
    print(inflater.needs_input(), inflater.finished())


