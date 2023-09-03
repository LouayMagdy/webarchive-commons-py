MAX_READ_SIZE = 128 * 1024


def copy(src: bytearray, offset=0, length=None) -> bytearray:
    if length is None:
        length = len(src)
    copy_arr = bytearray(length)
    copy_arr[:length] = src[offset:offset + length]
    return copy_arr


def cmp(input_arr: bytearray, wanted_arr: bytearray, src1: int = 0, src2: int = 0, n: int = None):
    if n is None:
        n = len(input_arr)
        if len(input_arr) != len(wanted_arr):
            return False
    elif src1 + n > len(input_arr) or src2 + n > len(wanted_arr):
        raise IndexError("Index out of bounds")
    for i in range(n):
        if input_arr[i + src1] != wanted_arr[i + src2]:
            return False
    return True

