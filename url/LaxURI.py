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
        self.uri = URICustom()

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
        self.uri.parseAuthority(original, escaped)
        if self.uri._host is not None and self.uri._authority is not None and len(self.uri._host) == len(self.uri._authority):
            self.uri._host = self.uri._authority

    def _set_uri(self):
        if self._scheme is not None:
            if len(self._scheme) == 4 and self._scheme == self.HTTP_SCHEME:
                self._scheme = self.HTTP_SCHEME
            elif len(self._scheme) == 5 and self._scheme == self.HTTPS_SCHEME:
                self._scheme = self.HTTPS_SCHEME
        self.setURI()

    def _parse_uri_reference(self, original: str, escaped: bool):
        if original is None:
            raise Exception("URI-Reference required")
        tmp: str = original.strip()
        length = len(tmp)
        if length > 0:
            first_delimiter = [tmp[0]]
            if self.validate(first_delimiter, URICustom._delims):
                if length >= 2:
                    last_delimiter = [tmp[length - 1]]
                    if self.validate(last_delimiter, URICustom._delims):
                        tmp = tmp[1:length - 1]
                        length = length - 2

        from_idx = 0
        is_started_from_path = False
        at_colon = tmp.index(':')
        at_slash = tmp.index('/')
        if not tmp.startswith("//") and (at_colon <= 0 or (0 <= at_slash < at_colon)):
            is_started_from_path = True

        at_idx = self.uri.index_first_of(tmp, "/?#" if is_started_from_path else ":/?#", from_idx)
        if at_idx == -1:
            at_idx = 0

        if 0 < at_idx < length and tmp[at_idx] == ':':
            target = tmp[0:at_idx].lower()
            if self.uri._validate(target, URICustom.scheme):
                self._scheme = target
                from_idx = at_idx + 1
                at_idx += 1
            else:
                # IA CHANGE: do nothing; allow interpretation as URI with later colon in other syntactical component
                pass

        self.uri._is_net_path = self.uri._is_abs_path = self.uri._is_rel_path = self.uri._is_hier_part = False
        if 0 <= at_idx < length and tmp[at_idx] == '/':
            self.uri._is_hier_part = True
            if at_idx+2 < length and tmp[at_idx+1] == '/' and not is_started_from_path:
                next_idx: int = self.uri.index_first_of(tmp, "/?#", at_idx+2)
                if next_idx == -1:
                    next_idx = at_idx+2 if len(tmp[at_idx+2:]) == 0 else len(tmp)
                self._parse_authority(tmp[at_idx+2:next_idx], escaped)
                from_idx = at_idx = next_idx
                self.uri._is_net_path = True
            if from_idx == at_idx:
                self.uri._is_abs_path = True

        if from_idx < length:
            next_idx = self.uri.index_first_of(tmp, "?#", from_idx)
            if next_idx == -1:
                next_idx = len(tmp)
            if not self.uri._is_abs_path:
                if not escaped and self.uri.prevalidate(tmp[from_idx:next_idx], URICustom._disallowed_rel_path) or \
                        escaped and self.uri.validate(tmp[from_idx:next_idx], URICustom._rel_path):
                    self.uri._is_rel_path = True
                elif not escaped and self.uri.prevalidate(tmp[from_idx, next_idx], URICustom._disallowed_opaque_part) or \
                    escaped and self.uri.validate(tmp[from_idx:next_idx], URICustom._opaque_part):
                    self.uri._is_opaque_part = True
                else:
                    self.uri._path = None
            s = tmp[from_idx: next_idx]
            if escaped:
                self.uri.set_raw_path(s)
            else:
                self.uri.set_path(s)
            at_idx = next_idx

        charset: str = self.uri.get_protocol_charset()
        if 0 <= at_idx and at_idx+1 < length and tmp[at_idx] == '?':
            next_idx2 = tmp.index('#', at_idx+1)
            if next_idx2 == -1:
                next_idx2 = len(tmp)
            if escaped:
                self.uri._query = tmp[at_idx+1:next_idx2]
                if not self.uri._validate(self.uri._query, URICustom.query):
                    raise Exception("Invalid query")
                else:
                    self.uri._query = self.uri.encode(tmp[at_idx+1:next_idx2], URICustom._allowed_query, charset)
                at_idx = next_idx2

        if 0 <= at_idx and at_idx+1 <= length and tmp[at_idx] == '#':
            if at_idx+1 == length:
                self.uri._fragment = ""
            else:
                self.uri._fragment = tmp[at_idx+1:] if escaped else self.uri.encode(tmp[at_idx+1:], URICustom._allowed_fragment, charset)
        self.uri.setURI()







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
