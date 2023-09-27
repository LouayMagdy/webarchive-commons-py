from bitarray import bitarray
import io
import codecs

class URLCodec:
    def __init__(self):
        self.WWW_FORM_URL = bitarray(256)
        self.WWW_FORM_URL.setall(False)

    def encode_url(self, urlsafe: bitarray, p_array: list):
        if p_array is None:
            return None
        else:
            if urlsafe is None:
                urlsafe = self.WWW_FORM_URL

            buffer = bytearray()
            for i in range(len(p_array)):
                b = p_array[i]
                if b >= 0 and urlsafe[b]:
                    if b == 32:
                        b = 43
                    buffer.append(b)
                else:
                    buffer.append(37)
                    hex1 = hex(b >> 4 & 15)[2:].upper()
                    hex2 = hex(b & 15)[2:].upper()
                    buffer.append(ord(hex1))
                    buffer.append(ord(hex2))
            return bytes(buffer)

    def decode_url(self, p_array):
        if p_array is None:
            return None
        else:
            buffer = io.BytesIO()
            for i in range(len(p_array)):
                b = p_array[i]
                if b == 43:
                    buffer.write(bytes([32]))
                elif b == 37:
                    try:
                        i+=1
                        u = int(chr(p_array[i]), 16)
                        i+=1
                        l = int(chr(p_array[i]), 16)
                        if u == -1 or l == -1:
                            raise Exception("Invalid URL encoding")
                        buffer.write(bytes([u << 4 + l]))
                    except IndexError:
                        raise Exception("Invalid URL encoding")
                else:
                    buffer.write(bytes([b]))
            return buffer.getvalue()
