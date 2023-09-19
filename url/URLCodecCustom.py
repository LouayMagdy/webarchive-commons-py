import urllib.parse
import io
from bitarray import bitarray

US_ASCII = "US-ASCII"
WWW_FORM_URL = bitarray(256)


class URLCodec:

    def __init__(self, encoding: str = "UTF-8"):
        self.encoding = encoding

    @staticmethod
    def encodeUrl(urlsafe: bitarray, p_array: bytearray):  # working function
        if p_array is None:
            return None
        else:
            if urlsafe is None:
                urlsafe = WWW_FORM_URL
            buffer = io.BytesIO()
            for i in range(len(p_array)):
                b = p_array[i]
                if b >= 0 and urlsafe[b]:
                    if b == 32:
                        b = 43
                    buffer.write(bytes([b]))
                else:
                    buffer.write(bytes([37]))
                    hex1 = hex(b >> 4 & 15)[2:].upper()
                    # hex1 = chr(b >> 4 & 15).upper()
                    hex2 = hex(b & 15)[2:].upper()
                    # hex2 = chr(b & 15).upper()
                    buffer.write(bytes([ord(hex1)]))
                    buffer.write(bytes([ord(hex2)]))
        return buffer.getvalue()

    @staticmethod
    def decodeUrl(pArray):
        if pArray is None:
            return None
        else:
            buffer = io.BytesIO()
            for i in range(len(pArray)):
                b = pArray[i]
                if b == 43:
                    buffer.write(bytes([32]))
                elif b == 37:
                    try:
                        i += 1
                        u_var = int(chr(pArray[i]), 16)
                        i += 1
                        l_var = int(chr(pArray[i]), 16)
                        if u_var == -1 or l_var == -1:
                            raise Exception("Invalid URL encoding")
                        buffer.write(bytes([u_var << 4 + l_var]))
                    except IndexError:
                        raise Exception("Invalid URL encoding")
                else:
                    buffer.write(bytes([b]))
            return buffer.getvalue()

    def encode(self, p_array: bytearray):
        return URLCodec.encodeUrl(WWW_FORM_URL, p_array)

    def decode(self, p_array: bytearray):
        return URLCodec.decodeUrl(p_array)


############# Testing #############

# urlsafe = bitarray(256)
# urlsafe.setall(False)
#
# my_input = bytearray('hello world'.encode())
# output = URLCodec.encodeUrl(urlsafe, my_input)
# for b in output:
#     print(b & 0xFF)
# print(str(output))


my_input2 = bytearray([72, 101, 108, 108, 111, 43, 87, 111, 114, 108, 100])
output2 = URLCodec.decodeUrl(my_input2)
for b in output2:
    print(b & 0xFF)
print(str(output2))
