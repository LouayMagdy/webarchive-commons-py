from URLCodecCustom import URLCodec
import io
from bitarray import bitarray


def initialize_default(cls):
    cls.DEFAULT = LaxURLCodec("UTF-8")
    return cls


def initialize_expanded_uri_safe(cls):
    cls.EXPANDED_URI_SAFE = bitarray(256)
    cls.EXPANDED_URI_SAFE.setall(False)
    for i in range(97, 123, 1):
        cls.EXPANDED_URI_SAFE[i] = True
    for i in range(65, 91, 1):
        cls.EXPANDED_URI_SAFE[i] = True
    for i in range(48, 58, 1):
        cls.EXPANDED_URI_SAFE[i] = True
    cls.EXPANDED_URI_SAFE[ord('-')] = True
    cls.EXPANDED_URI_SAFE[ord('~')] = True
    cls.EXPANDED_URI_SAFE[ord('_')] = True
    cls.EXPANDED_URI_SAFE[ord('.')] = True
    cls.EXPANDED_URI_SAFE[ord('*')] = True
    cls.EXPANDED_URI_SAFE[ord('/')] = True
    cls.EXPANDED_URI_SAFE[ord('=')] = True
    cls.EXPANDED_URI_SAFE[ord('&')] = True
    cls.EXPANDED_URI_SAFE[ord('+')] = True
    cls.EXPANDED_URI_SAFE[ord(',')] = True
    cls.EXPANDED_URI_SAFE[ord(':')] = True
    cls.EXPANDED_URI_SAFE[ord(';')] = True
    cls.EXPANDED_URI_SAFE[ord('@')] = True
    cls.EXPANDED_URI_SAFE[ord('$')] = True
    cls.EXPANDED_URI_SAFE[ord('!')] = True
    cls.EXPANDED_URI_SAFE[ord(')')] = True
    cls.EXPANDED_URI_SAFE[ord('(')] = True
    cls.EXPANDED_URI_SAFE[ord('%')] = True
    cls.EXPANDED_URI_SAFE[ord('|')] = True
    cls.EXPANDED_URI_SAFE[ord('\'')] = True
    return cls


def initialize_query_safe(cls):
    cls.QUERY_SAFE = bitarray(256)
    cls.QUERY_SAFE.setall(False)
    cls.QUERY_SAFE[:] |= cls.EXPANDED_URI_SAFE[:]
    cls.QUERY_SAFE[ord('{')] = True
    cls.QUERY_SAFE[ord('}')] = True
    cls.QUERY_SAFE[ord('[')] = True
    cls.QUERY_SAFE[ord(']')] = True
    cls.QUERY_SAFE[ord('^')] = True
    cls.QUERY_SAFE[ord('?')] = True
    return cls


@initialize_query_safe
@initialize_expanded_uri_safe
class LaxURLCodec(URLCodec):
    DEFAULT = None
    EXPANDED_URI_SAFE = None
    QUERY_SAFE = None

    def __init__(self, encoding: str = "UTF-8"):
        super().__init__(encoding)

    def decode_url_loose(self, bytes: bytearray):
        if bytes is None:
            return None
        else:
            buffer = io.BytesIO()
            for i in range(len(bytes)):
                b = bytes[i]
                if b == 43:
                    buffer.write(32)  # space character
                elif b == 37:
                    if i+2 < len(bytes):
                        u_var = int(chr(bytes[i+1]), 16)
                        l_var = int(chr(bytes[i+2]), 16)
                        if u_var>-1 and l_var>-1:
                            c = u_var << 4 + l_var
                            buffer.write(c)
                            i += 2
                            continue
                buffer.write(b)
            return buffer.getvalue()

    def encode(self, safe: bitarray, p_string: str, cs: str) -> str:
        if p_string is None:
            return None
        return str(URLCodec.encodeUrl(safe, bytearray(p_string.encode(cs))), cs)


# lol = LaxURLCodec()
# print(lol)
