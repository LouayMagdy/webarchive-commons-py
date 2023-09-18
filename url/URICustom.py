from bitarray import bitarray
from urllib.parse import urlparse, quote, urlsplit, urlunsplit, urlunparse


def initialize_reserved(cls):
    cls._reserved = bitarray(256)
    cls._reserved.setall(False)
    cls._reserved[ord(';')] = True
    cls._reserved[ord('/')] = True
    cls._reserved[ord('?')] = True
    cls._reserved[ord(':')] = True
    cls._reserved[ord('@')] = True
    cls._reserved[ord('&')] = True
    cls._reserved[ord('=')] = True
    cls._reserved[ord('+')] = True
    cls._reserved[ord('$')] = True
    cls._reserved[ord(',')] = True
    return cls


def initialize_uric(cls):
    cls._uric = bitarray(256)
    cls._uric.setall(False)
    cls._uric[:] |= cls._reserved[:]
    cls._uric[:] |= cls._unreserved[:]
    cls._uric[:] |= cls._escaped[:]
    return cls


def initialize_query(cls):
    cls._query = cls._uric


def initialize_abs_path(cls):
    cls._abs_path = bitarray(256)
    cls._abs_path.setall(False)
    cls._abs_path[ord('/')] = True
    cls._abs_path[:] |= cls._path_segments[:]
    return cls


def initialize_path_segments(cls):
    cls._path_segments = bitarray(256)
    cls._path_segments.setall(False)
    cls._path_segments[:] |= cls._segment[:]
    cls._path_segments[ord('/')] = True
    return cls


def initialize_segment(cls):
    cls._segment = bitarray(256)
    cls._segment.setall(False)
    cls._segment[:] |= cls._pchar[:]
    cls._segment[ord(';')] = True
    cls._segment[:] |= cls._param[:]
    return cls


def initialize_pchar(cls):
    cls._pchar = bitarray(256)
    cls._pchar.setall(False)
    cls._pchar[:] |= cls._unreserved[:]
    cls._pchar[:] |= cls._escaped[:]
    cls._pchar[ord(':')] = True
    cls._pchar[ord('@')] = True
    cls._pchar[ord('&')] = True
    cls._pchar[ord('=')] = True
    cls._pchar[ord('+')] = True
    cls._pchar[ord('$')] = True
    cls._pchar[ord(',')] = True
    return cls


def initialize_param(cls):
    cls._param = cls._pchar
    return cls


def initialize_rel_segment(cls):
    cls._rel_segment = bitarray(256)
    cls._rel_segment.setall(False)
    cls._rel_segment[:] |= cls._unreserved[:]
    cls._rel_segment[:] |= cls._escaped[:]
    cls._rel_segment[ord(';')] = True
    cls._rel_segment[ord('@')] = True
    cls._rel_segment[ord('&')] = True
    cls._rel_segment[ord('=')] = True
    cls._rel_segment[ord('+')] = True
    cls._rel_segment[ord('$')] = True
    cls._rel_segment[ord(',')] = True
    return cls


def initialize_unreserved(cls):
    cls._unreserved = bitarray(256)
    cls._unreserved.setall(False)
    cls._unreserved[:] |= cls._alphanum[:]
    cls._unreserved[:] |= cls._mark[:]
    return cls


def initialize_alphanum(cls):
    cls._alphanum = bitarray(256)
    cls._alphanum.setall(False)
    cls._alphanum[:] |= cls._alpha[:]
    cls._alphanum[:] |= cls._digit[:]
    return cls


def initialize_alpha(cls):
    cls._alpha = bitarray(256)
    cls._alpha.setall(False)
    for i in range(97, 123, 1):
        cls._alpha.__setitem__(i, True)
    for i in range(65, 91, 1):
        cls._alpha.__setitem__(i, True)
    return cls


def initialize_digit(cls):
    cls._digit = bitarray(256)
    cls._digit.setall(False)
    for i in range(48, 58, 1):
        cls._digit.__setitem__(i, True)
    return cls


def initialize_mark(cls):
    cls._mark = bitarray(256)
    cls._mark.setall(False)
    cls._mark[ord('-')] = True
    cls._mark[ord('_')] = True
    cls._mark[ord('.')] = True
    cls._mark[ord('!')] = True
    cls._mark[ord('~')] = True
    cls._mark[ord('*')] = True
    cls._mark[ord('\'')] = True
    cls._mark[ord('(')] = True
    cls._mark[ord(')')] = True
    return cls


def initialize_escaped(cls):
    cls._escaped = bitarray(256)
    cls._escaped.setall(False)
    cls._escaped[:] |= cls._percent[:]
    cls._escaped[:] |= cls._hex[:]
    return cls


def initialize_percent(cls):
    cls._percent = bitarray(256)
    cls._percent.setall(False)
    cls._percent[ord('%')] = True
    return cls


def initialize_hex(cls):
    cls._hex = bitarray(256)
    cls._hex.setall(False)
    cls._hex[:] |= cls._digit[:]
    for i in range(97, 103, 1):
        cls._hex.__setitem__(i, True)
    for i in range(65, 71, 1):
        cls._hex.__setitem__(i, True)
    return cls


def initialize(cls):
    initialize_alpha(cls)
    initialize_digit(cls)

    initialize_mark(cls)
    initialize_alphanum(cls)

    initialize_percent(cls)
    initialize_hex(cls)

    initialize_escaped(cls)
    initialize_unreserved(cls)

    initialize_reserved(cls)
    initialize_uric(cls)
    initialize_query(cls)

    initialize_pchar(cls)
    initialize_param(cls)

    initialize_segment(cls)
    initialize_path_segments(cls)
    initialize_abs_path(cls)

    initialize_rel_segment(cls)

    return cls


@initialize
class URICustom:
    def __init__(self, s: str = None, strict: bool = False, charset: str = None):
        self.protocol_charset = charset
        



def check():
    b = bitarray(256)
    b.setall(False)
    print(b)
    for i in range(48, 58, 1):
        b.__setitem__(i, True)
    print(b)



uri = URICustom()
# print(uri.ay7aga)
print(URICustom._lax_rel_segment)
# check()
