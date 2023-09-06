import os
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

with open('./experimental/writing_short.txt', 'rb') as f_i:
    print(f_i.read(2))
    print(f_i.read(2))
    print(f_i.read(5))

