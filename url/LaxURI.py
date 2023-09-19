from urllib.parse import urlparse, urlunparse
from bitarray import bitarray
from URICustom import URICustom
from urllib.parse import urlparse, quote, urlsplit, urlunsplit, urlunparse


def initialize_lax_rel_segment(cls):
    cls._lax_rel_segment = bitarray(256)
    cls._lax_rel_segment.setall(False)
    cls._lax_rel_segment[:] |= cls._rel_segment[:]
    cls._lax_rel_segment[ord(':')] = True
    # TODO: add additional allowances as need is demonstrated
    return cls


def initialize_lax_abs_path(cls):
    cls._lax_abs_path = bitarray(256)
    cls._lax_abs_path.setall(False)
    cls._lax_abs_path[:] |= cls._abs_path[:]
    cls._lax_abs_path[ord('|')] = True
    return cls


def initialize_lax_rel_path(cls):
    cls._lax_rel_path = bitarray(256)
    cls._lax_rel_path.setall(False)
    cls._lax_rel_path[:] |= cls._lax_rel_segment[:]
    cls._lax_rel_path[:] |= cls._lax_abs_path[:]
    return cls


def initialize_lax_query(cls):
    cls._lax_query = bitarray(256)
    cls._lax_query.setall(False)
    cls._lax_query[:] |= cls._query[:]  # inherited from URICustom
    cls._lax_query[ord('{')] = True
    cls._lax_query[ord('}')] = True
    cls._lax_query[ord('|')] = True
    cls._lax_query[ord('[')] = True
    cls._lax_query[ord(']')] = True
    cls._lax_query[ord('^')] = True
    return cls


def initialize(cls):
    initialize_lax_rel_segment(cls)
    initialize_lax_abs_path(cls)
    initialize_lax_rel_path(cls)
    initialize_lax_query(cls)


@initialize
class LaxURI(URICustom):  # in java: extends URI
    # serial_version_UID = 5273922211722239537
    HTTP_SCHEME = ['h', 't', 't', 'p']
    HTTPS_SCHEME = ['h', 't', 't', 'p', 's']
    lax_rel_segment = None
    lax_abs_path = None
    lax_rel_path = None
    lax_query = None

    def __init__(self):
        super().__init__()

    print(lax_query)


    # rel_segment = bitarray()
    # lax_rel_segment |= rel_segment
    # lax_rel_segment[ord(':')] = True





############## TO BE CONTINUED WHEN I UNDERSTAND WHAT IT DOES! ######################


lol = LaxURI()

# rel_segment = bitarray(256)
# rel_segment[b'a'] = 1
# rel_segment[b'b'] = 1
# rel_segment[b'c'] = 1
# rel_segment[b'd'] = 1
#
# lax_rel_segment = bytearray(256)
# lax_rel_segment[:] = rel_segment
# lax_rel_segment[b':'] = 1
#
# print(bool(lax_rel_segment[b'a']))
# print(bool(lax_rel_segment[b'b']))
# print(bool(lax_rel_segment[b'c']))
# print(bool(lax_rel_segment[b'd']))
# print(bool(lax_rel_segment[b':']))
# print(bool(lax_rel_segment[b'e']))
#


