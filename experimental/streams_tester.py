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

# testing Decoder
# from utils.CRC32 import CRC32
# with open('./experimental/writing_short.txt', 'wb') as f_o:
#     crc = CRC32()
#     f_o.write(bytearray([12, 23, 0x1f, 0x8b, 0x1f, 0x8b, 0x08, 0x04, 0, 0, 0, 0, 0, 0]))
#     f_o.write(bytearray([0xf, 0, 0x65, 0x66, 0, 0, 12, 54, 68]))
#     f_o.write(bytearray([0x84, 0x66, 4, 0, 12, 54, 68, 64]))
#     f_o.write(bytearray([0x78, 0x57, 0x00]))
#     f_o.write(bytearray([0x78, 0x57, 34, 23, 98, 0x00]))
#
# from formats.gzip.GZIPDecoder import GZIPDecoder
# from experimental.simple_is import SimpleIS
#
# with open('./experimental/writing_short.txt', 'rb') as f_i:
#     decoder = GZIPDecoder(max_name_size=1024)
#     simple_is = SimpleIS(f_i)
#     skipped = decoder.align_on_magic3(simple_is)
#     # print(f"skipped = {skipped}", f"{decoder.is_aligned_at_eof(skipped)}")
#     decoder.parse_header(orig_input_stream=simple_is, assume1st3=True)

import mmap
from streamcontext.RandomAccessFileStream import RandomAccessFileStream
from streamcontext.HTTP11Stream import HTTP11Stream
from streamcontext.HDFSStream import HDFSStream

# rfa = RandomAccessFileStream(open("./experimental/writing_short.txt", 'rb'))
# b = bytearray(100)
# print(b)
# print(rfa.read(b, 0, 10), b)
# print(f"Curr offset: {rfa.get_offset()}")
# rfa.set_offset(20)
# print(rfa.read(b, 0, 10), b)
# print(f"Curr offset: {rfa.get_offset()}")
# rfa.set_offset(0)
# print(rfa.read(b, 0, 400), b)

# b = bytearray(610)
# hdfs = HDFSStream("http://10.35.139.54:9870", "/text_files/text_1.txt")
# print(b)
# print(hdfs.read(b, 0, 100), b)
# print(f"curr. offset: {hdfs.get_offset()}")
# hdfs.set_offset(100)
# print(hdfs.read(b, 100, 100), b)
# print(f"curr. offset: {hdfs.get_offset()}")
# hdfs.set_offset(0)
# print(hdfs.read(b, 0, 610), b)

# b = bytearray(100)
# hs = HTTP11Stream("http://i.imgur.com/z4d4kWk.jpg")
# print(hs.read(b, 0, 10), b)
# print(f"Curr offset: {hs.get_offset()}")
# hs.set_offset(20)
# print(hs.read(b, 0, 50), b)
# print(f"Curr offset: {hs.get_offset()}")
# hs.set_offset(1000)
# print(hs.read(b, 0, 95), b)
# print(f"Curr offset: {hs.get_offset()}")


# with open("./experimental/writing_short.txt", 'rb') as f_i:
#     file_name = os.path.basename(f_i.name)
#     print(file_name)
#
# from urllib.parse import urlparse
#
# url = 'http://10.0.0.1:8080/path/to/file.txt'
# url = "http://i.imgur.com/z4d4kWk.jpg"
# parsed_url = urlparse(url)
# scheme = parsed_url.scheme
# netloc = parsed_url.netloc
# path = parsed_url.path
# filename = path.split('/')[-1]
# print('Scheme:', scheme)
# print('Netloc:', netloc)
# print('Path:', path)
# print('Filename:', filename)
