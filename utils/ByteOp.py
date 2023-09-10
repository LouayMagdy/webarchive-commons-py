import os
import math

MAX_READ_SIZE = 128 * 1024


def copy(src: bytearray, offset=0, length=None) -> bytearray:
    if length is None:
        length = len(src)
    copy_arr = bytearray(length)
    copy_arr[:length] = src[offset:offset + length]
    return copy_arr


def cmp(input_arr: bytearray, wanted_arr: bytearray, src1: int = 0, src2: int = 0, n: int = None) -> bool:
    if n is None:
        if len(input_arr) != len(wanted_arr):
            return False
        else:
            n = len(input_arr)
    if src1 + n > len(input_arr) or src2 + n > len(wanted_arr):
        raise IndexError("Index out of bounds")
    for i in range(n):
        if input_arr[i + src1] != wanted_arr[i + src2]:
            return False
    return True


def append(a: bytearray, b: bytearray) -> bytearray:
    res = bytearray(len(a) + len(b))
    res[:len(a)] = a[:]
    res[len(a):] = b[:]
    return res


def bytes_to_short(b1: int = None, b2: int = None, byte_arr: bytearray = None, offset: int = 0):
    if not (b1 is None or b2 is None):
        return ((b2 << 8) & 0x00ff00) | (b1 & 0xff)
    elif byte_arr is not None:
        if len(byte_arr) - offset < 2:
            raise IndexError("Index out of bounds")
        return bytes_to_short(byte_arr[offset], byte_arr[offset + 1])


def read_short(input_stream):
    b1 = bytearray(input_stream.read())
    if b1 == b'':
        raise EOFError("No bytes expected short(2)")
    b1 = b1[0] & 0xff
    b2 = bytearray(input_stream.read())
    if b2 == b'':
        raise EOFError("No bytes expected short(2)")
    b2 = b2[0] & 0xff
    return bytes_to_short(b1, b2)


def write_short(short_val, output_stream=None, buffer: bytearray = None, offset=0):
    if output_stream is not None:
        buff = bytearray([short_val & 0xff, ((short_val & 0x00ff00) >> 8) & 0xff])
        output_stream.write(buff)
    elif buffer is not None:
        if len(buffer) - offset < 2:
            raise IndexError("Index out of bounds")
        buffer[offset] = short_val & 0xff
        buffer[offset + 1] = ((short_val & 0x00ff00) >> 8) & 0xff


def bytes_to_int(b1: int = None, b2: int = None, b3: int = None,
                 b4: int = None, byte_arr: bytearray = None, offset: int = 0):
    if not (b1 is None or b2 is None or b3 is None or b4 is None):
        return (b1 & 0xff) | ((b2 << 8) & 0x00ff00) | ((b3 << 16) & 0x00ff0000) | ((b4 << 24) & 0xff000000)
    elif byte_arr is not None:
        if len(byte_arr) - offset < 4:
            raise IndexError("Index out of bounds")
        return bytes_to_int(byte_arr[offset], byte_arr[offset + 1], byte_arr[offset + 2], byte_arr[offset + 3])


def read_int(input_stream):
    buff = bytearray(input_stream.read(4))
    for i in range(4):
        if buff[i] == b'':
            raise EOFError("No bytes expected Int(4)")
    b1 = buff[0] & 0xff
    b2 = buff[1] & 0xff
    b3 = buff[2] & 0xff
    b4 = buff[3] & 0xff
    return bytes_to_int(b1, b2, b3, b4)


def write_int(int_val, output_stream=None, buffer: bytearray = None, offset=0):
    if output_stream is not None:
        buff = bytearray([int_val & 0xff, ((int_val & 0x00ff00) >> 8) & 0xff,
                          (((int_val & 0x00ff0000) >> 16) & 0xff), (((int_val & 0x00ff000000) >> 24) & 0xff)])
        output_stream.write(buff)
    elif buffer is not None:
        if len(buffer) - offset < 4:
            raise IndexError("Index out of bounds")
        buffer[offset] = int_val & 0xff
        buffer[offset + 1] = ((int_val & 0x00ff00) >> 8) & 0xff
        buffer[offset + 2] = ((int_val & 0x00ff0000) >> 16) & 0xff
        buffer[offset + 3] = ((int_val & 0x00ff000000) >> 24) & 0xff


def read_n_bytes(input_stream, n: int) -> bytearray:
    buff = bytearray(n)
    left = n
    curr_pos = input_stream.tell()
    while left:
        input_stream.seek(curr_pos + n - left)
        buff[(n - left):] = input_stream.read(length=left)
        if len(buff) < left:
            raise EOFError("Short read")
        left -= len(buff)
    return buff


def read_to_null(input_stream, max_size=MAX_READ_SIZE) -> bytearray:
    byte_arr = bytearray(max_size)
    for i in range(max_size):
        b = bytearray(input_stream.read())[0] & 0xff
        byte_arr[i] = b
        if not b:
            return copy(byte_arr, 0, i + 1)
        if i + 1 == max_size and i + 1 == os.fstat(input_stream.fileno()).st_size:
            raise EOFError("NO NULL")
    raise IOError("Buffer too small")


def discard_to_null(input_stream) -> int:
    i = 0
    while 1:
        b = bytearray(input_stream.read())[0] & 0xff
        i += 1
        if not b:
            return i
        if i == os.fstat(input_stream.fileno()).st_size:
            raise EOFError("No NULL before EOF")


def draw_hex(byte_arr: bytearray, offset=0, length=None, bytes_per_row=None):
    if length is None:
        length = len(byte_arr)
    if bytes_per_row is None:
        bytes_per_row = length
    num_rows = math.ceil(length / bytes_per_row)
    if not num_rows:
        num_rows = 1
    bytes_to_output = length
    position = 0
    # 2 chars per byte, plus 1 space, plus 1 newline per row:
    string_builder = []
    for row in range(num_rows):
        bytes_this_row = min(bytes_to_output, bytes_per_row)
        for col in range(bytes_this_row):
            hex_string = hex(byte_arr[position] & 0xff)[2:]
            position += 1
            if len(hex_string) == 2:
                string_builder.append(hex_string)
            else:
                string_builder.append("0")
                string_builder.append(hex_string)
        bytes_to_output -= bytes_this_row
        string_builder.append('\n') # this line may need to be removed
    return string_builder


def read_file(file_stream) -> bytearray:
    file_length = os.fstat(file_stream.fileno()).st_size
    if file_length > (2 ** 31 - 1):
        raise IOError("File too big to read into buffer..")
    return read_n_bytes(file_stream, file_length)

# x = bytearray([4, 2, 4, 6])
# print(x.find(10))
# y = bytearray([3, 2, 4])
# print(cmp(x, y), cmp(x, y, 1, 1))
# print(x, copy(x), cmp(x, copy(x)))
# print(append(x, y))
# print(bytes_to_short(1, 1), bytes_to_short(byte_arr=bytearray([2, 1, 1])))

# with open('./experimental/writing_short.txt', 'wb') as f_o:
#     write_int(2 ** 31 - 1, f_o)
#     f_o.close()

# with open('./experimental/writing_short.txt', 'rb') as f_i:
    # print(read_short(f_i))
    # print(read_int(f_i))
    # print(read_n_bytes(f_i, 4))
    # print(read_to_null(f_i, 4))
    # print(discard_to_null(f_i))
    # print(read_file(f_i))

# buffer = bytearray(4)
# write_int(2**31 - 1, buffer=buffer)
# print(buffer)

# byte_arr = bytearray([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])
# res = draw_hex(byte_arr, length=len(byte_arr), bytes_per_row=math.ceil(len(byte_arr) / 2))
# print(''.join(res))
