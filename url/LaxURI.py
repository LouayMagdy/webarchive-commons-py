from urllib.parse import urlparse, urlunparse
from bitarray import bitarray
from URICustom import URICustom
from urllib.parse import urlparse, unquote, urlsplit, urlunsplit, urlunparse

from url.LaxURLCodec import LaxURLCodec


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
    return cls


def decode(component: list, charset: str):
    if component is None:
        raise ValueError("Component array of chars may not be null")

    component = "".join(component)  # converting component from list of chars to string
    if component is None:
        raise ValueError("Component array of chars may not be null")
    rawdata: bytearray = lax_url_codec.decode_url_loose(
        component.encode('ascii'))  # expected bytearray, got bytes instead
    return rawdata.decode(charset)


lax_url_codec = LaxURLCodec()


@initialize
class LaxURI(URICustom):  # in java: extends URI
    # serial_version_UID = 5273922211722239537
    HTTP_SCHEME = ['h', 't', 't', 'p']
    HTTPS_SCHEME = ['h', 't', 't', 'p', 's']

    def __init__(self):  # in java: multiple constructors are made, and will be made here JUST if needed!
        super().__init__()

    def get_uri(self) -> str:
        return None if self._uri is None else LaxURI.decode(self._uri, LaxURI.get_protocol_charset())

    ## We need to find an alternative, because this requires too built-in parts ofthe java URI class!
    # def get_path(self) -> str:
    #    p =

    def validate(self, component, generous, s_offset: int = -1, e_offset: int = -1):
        if s_offset == -1 and e_offset == -1:
            return self._validate(component, self._lax(generous))
        return self._validate_helper(component, s_offset, e_offset, self._lax(generous))

    def _lax(self, generous):
        if generous == URICustom._rel_segment:
            return LaxURI._lax_rel_segment
        if generous == URICustom._abs_path:
            return LaxURI._lax_abs_path
        if generous == URICustom._query:
            return LaxURI._lax_query
        if generous == URICustom._rel_path:
            return LaxURI._lax_rel_path
        return generous

    def _parse_authority(self, original: str, escaped: bool):
        # Decode the original string if it is escaped
        if escaped:
            original = unquote(original)
        # Parse the URI and get the authority component
        parsed_uri = urlparse(original)
        authority = parsed_uri.netloc

    def _set_uri(self):
        pass

    def _parse_uri_reference(self, original: str, escaped: bool):
        pass


print(LaxURI._lax_rel_segment)
print(LaxURI._lax_query)
print(LaxURI._lax_abs_path)
print(LaxURI._lax_rel_path)
print(LaxURI.HTTP_SCHEME)

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
