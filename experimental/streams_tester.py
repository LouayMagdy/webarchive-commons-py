import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

def dump(output_stream, input_stream):
    output_stream.write(input_stream.read().decode())


def dump_short(output_stream, input_stream):
    byte_count = 0
    chunk_size = 3
    while True:
        chunk = input_stream.read(chunk_size)
        arr = bytearray(chunk_size)
        arr[:] = chunk
        print(chunk, arr)
        if len(arr) > 1:
            print(arr[0] & 0xff)
        if not chunk:
            break
        byte_count += len(chunk)
    output_stream.write(f"\nResource Was: {byte_count} Long\n")


# with open("./experimental/my_dict.json", "rb") as inp, open("./experimental/stream.txt", "w") as outp:
#     dump(outp, inp)
# with open("./experimental/my_dict.json", "rb") as inp, open("./experimental/stream.txt", "a") as outp:
    # dump_short(outp, inp)
# with open("./experimental/my_dict.json", "rb") as f_i:
#     print(os.fstat(f_i.fileno()).st_size)

from utils.CRC32 import CRC32
with open('./experimental/writing_short.txt', 'wb') as f_o:
    crc = CRC32()
    f_o.write(bytearray([12, 23, 0x1f, 0x8b, 0x1f, 0x8b, 0x08, 0x04, 0, 0, 0, 0, 0, 0]))
    f_o.write(bytearray([0xf, 0, 0x65, 0x66, 0, 0, 12, 54, 68]))
    f_o.write(bytearray([0x84, 0x66, 4, 0, 12, 54, 68, 64]))
    f_o.write(bytearray([0x78, 0x57, 0x00]))
    f_o.write(bytearray([0x78, 0x57, 34, 23, 98, 0x00]))

from formats.gzip.GZIPDecoder import GZIPDecoder
from experimental.simple_is import SimpleIS

with open('./experimental/writing_short.txt', 'rb') as f_i:
    decoder = GZIPDecoder(max_name_size=1024)
    simple_is = SimpleIS(f_i)
    skipped = decoder.align_on_magic3(simple_is)
    # print(f"skipped = {skipped}", f"{decoder.is_aligned_at_eof(skipped)}")
    decoder.parse_header(orig_input_stream=simple_is, assume1st3=True)

