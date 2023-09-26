from bitarray import bitarray

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