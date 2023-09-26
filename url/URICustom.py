from bitarray import bitarray
from urllib.parse import urlparse, quote, urlsplit, urlunsplit, urlunparse
import urllib.parse
from URLCodec import URLCodec
import logging
import codecs


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
    cls.query = cls._uric


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


def initialize_toplabel(cls):
    cls._toplabel = bitarray(256)
    cls._toplabel.setall(False)
    cls._toplabel[:] |= cls._alphanum[:]
    cls._toplabel[ord('-')] = True
    return cls


def initialize_hostname(cls):
    cls._hostname = bitarray(256)
    cls._hostname.setall(False)
    cls._hostname[:] |= cls._toplabel[:]
    cls._hostname[ord('-')] = True
    return cls


def initialize_reg_name(cls):
    cls._reg_name = bitarray(256)
    cls._reg_name.setall(False)
    cls._reg_name[:] |= cls._unreserved[:]
    cls._reg_name[:] |= cls._escaped[:]
    cls._reg_name[ord('$')] = True
    cls._reg_name[ord(',')] = True
    cls._reg_name[ord(';')] = True
    cls._reg_name[ord(':')] = True
    cls._reg_name[ord('@')] = True
    cls._reg_name[ord('&')] = True
    cls._reg_name[ord('=')] = True
    cls._reg_name[ord('+')] = True
    return cls


def initialize_IPv4address(cls):
    cls._IPv4address = bitarray(256)
    cls._IPv4address.setall(False)
    cls._IPv4address[:] |= cls._digit[:]
    cls._IPv4address[ord('.')] = True
    return cls


def initialize_IPv6address(cls):
    cls._IPv6address = bitarray(256)
    cls._IPv6address.setall(False)
    cls._IPv6address[:] |= cls._hex[:]
    cls._IPv6address[ord(':')] = True
    cls._IPv6address[:] |= cls._IPv4address[:]
    return cls


def initialize_allowed_reg_name(cls):
    cls._allowed_reg_name = bitarray(256)
    cls._allowed_reg_name.setall(False)
    cls._allowed_reg_name[:] |= cls._reg_name[:]
    cls._allowed_reg_name[ord('%')] = False
    return cls


def initialize_userinfo(cls):
    cls._userinfo = bitarray(256)
    cls._userinfo.setall(False)
    cls._userinfo[:] |= cls._unreserved[:]
    cls._userinfo[:] |= cls._escaped[:]
    cls._userinfo[ord(';')] = True
    cls._userinfo[ord(':')] = True
    cls._userinfo[ord('&')] = True
    cls._userinfo[ord('=')] = True
    cls._userinfo[ord('+')] = True
    cls._userinfo[ord('$')] = True
    cls._userinfo[ord(',')] = True
    return cls


def initialize_allowed_userinfo(cls):
    cls._allowed_user_info = bitarray(256)
    cls._allowed_user_info.setall(False)
    cls._allowed_user_info[:] |= cls._userinfo[:]
    cls._allowed_user_info[ord('%')] = False


def initialize_delims(cls):
    cls._delims = bitarray(256)
    cls._delims.setall(False)
    cls._delims[ord('<')] = True
    cls._delims[ord('>')] = True
    cls._delims[ord('#')] = True
    cls._delims[ord('%')] = True
    cls._delims[ord('"')] = True
    return cls


def initialize_scheme(cls):
    cls.scheme = bitarray(256)
    cls.scheme.setall(False)
    cls.scheme[:] |= cls._alpha[:]
    cls.scheme[:] |= cls._digit[:]
    cls.scheme[ord('+')] = True
    cls.scheme[ord('-')] = True
    cls.scheme[ord('.')] = True
    return cls


def initialize_disallowed_rel_path(cls):
    cls._disallowed_rel_path = bitarray(256)
    cls._disallowed_rel_path.setall(False)
    cls._disallowed_rel_path[:] |= cls._uric[:]
    cls._disallowed_rel_path[:] &= ~cls._rel_path[:]
    return cls


def initialize_uric_no_slash(cls):
    cls._uric_no_slash = bitarray(256)
    cls._uric_no_slash.setall(False)
    cls._uric_no_slash[:] |= cls._unreserved[:]
    cls._uric_no_slash[:] |= cls._escaped[:]
    cls._uric_no_slash[ord(';')] = True
    cls._uric_no_slash[ord('?')] = True
    cls._uric_no_slash[ord(':')] = True
    cls._uric_no_slash[ord('@')] = True
    cls._uric_no_slash[ord('&')] = True
    cls._uric_no_slash[ord('=')] = True
    cls._uric_no_slash[ord('+')] = True
    cls._uric_no_slash[ord('$')] = True
    cls._uric_no_slash[ord(',')] = True
    return cls


def initialize_opaque_part(cls):
    cls._opaque_part = bitarray(256)
    cls._opaque_part.setall(False)
    cls._opaque_part[:] |= cls._uric_no_slash[:]
    cls._opaque_part[:] |= cls._uric[:]
    return cls


def initialize_disallowed_opaque_part(cls):
    cls._disallowed_opaque_part = bitarray(256)
    cls._disallowed_opaque_part.setall(False)
    cls._disallowed_opaque_part[:] |= cls._uric[:]
    cls._disallowed_opaque_part[:] &= ~cls._opaque_part[:]
    return cls


def initialize_allowed_query(cls):
    cls._allowed_query = bitarray(256)
    cls._allowed_query.setall(False)
    cls._allowed_query[:] |= cls._uric[:]
    cls._allowed_query[ord('%')] = False
    return cls


def initialize_allowed_fragment(cls):
    cls._allowed_fragment = bitarray(256)
    cls._allowed_fragment.setall(False)
    cls._allowed_fragment[:] |= cls._uric[:]
    cls._allowed_fragment[ord('%')] = False
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
    initialize_toplabel(cls)
    initialize_hostname(cls)
    initialize_reg_name(cls)
    initialize_IPv4address(cls)

    initialize_IPv6address(cls)
    initialize_allowed_reg_name(cls)
    initialize_userinfo(cls)
    initialize_allowed_userinfo(cls)

    initialize_uric_no_slash(cls)
    initialize_opaque_part(cls)

    initialize_delims(cls)
    initialize_scheme(cls)
    initialize_disallowed_rel_path(cls)
    initialize_disallowed_opaque_part(cls)
    initialize_allowed_query(cls)
    initialize_allowed_fragment(cls)

    return cls


@initialize
class URICustom:
    def __init__(self, s: str = None, strict: bool = False, charset: str = None):
        self._authority = None
        self.protocol_charset = charset
        self._uri:list = []
        self._opaque:list = []
        self.authority = None
        self._host = None
        self._is_reg_name: bool = False
        self._is_server: bool = False
        self._is_hostname: bool = False
        self._is_IPv4address: bool = False
        self._is_IPv6reference: bool = False
        self._is_opaque_part: bool = True
        self._port: int = -1
        self._scheme: list = []
        self.is_net_path: bool = False
        self.is_abs_path: bool = False
        self.is_rel_path: bool = False
        self.is_hier_part: bool = False
        self._is_opaque_part: bool = False
        self._path: list = []
        self._query: list = []
        self.hash = 0
        self._fragment: list = []
        self.LOG = logging.getLogger(__name__)

    def parseAuthority(self, original, escaped):
        # Reset flags
        self._is_reg_name = self._is_server = self._is_hostname = self._is_IPv4address = self._is_IPv6reference = False

        # set the charset to do escape encoding
        charset = 'utf-8'  # You can change this to your desired charset

        hasPort = True
        from_index = 0
        next_index = original.find('@')
        if next_index != -1:
            userinfo = original[:next_index] if escaped else urllib.parse.quote(original[:next_index], safe=URICustom._allowed_userinfo)
            URICustom._userinfo = userinfo.encode(charset)
            from_index = next_index + 1

        next_index = original.find('[', from_index)
        if next_index >= from_index:
            next_index = original.find(']', from_index)
            if next_index == -1:
                raise Exception("IPv6reference")
            else:
                next_index += 1
            # In IPv6reference, '[', ']' should be excluded
            self._host = original[from_index:next_index] if escaped else urllib.parse.quote(original[from_index:next_index], safe=URICustom._allowed_IPv6reference)
            # Set flag
            self._is_IPv6reference = True
        else:  # only for !_is_IPv6reference
            next_index = original.find(':', from_index)
            if next_index == -1:
                next_index = len(original)
                hasPort = False
            # REMINDME: it doesn't need the pre-validation
            self._host = original[from_index:next_index].encode(charset)
            if self._validate(self._host, URICustom._IPv4address):
                # Set flag
                self._is_IPv4address = True
            elif self._validate(self._host, URICustom._hostname):
                # Set flag
                self._is_hostname = True
            else:
                # Set flag
                self._is_reg_name = True

        if self._is_reg_name:
            # Reset flags for a server-based naming authority
            self._is_server = self._is_hostname = self._is_IPv4address = self._is_IPv6reference = False
            # set a registry-based naming authority
            if escaped:
                self._authority = original.encode(charset)
                if not self._validate(self._authority, URICustom._reg_name):
                    raise Exception("Invalid authority")
            else:
                self._authority = urllib.parse.quote(original, safe=URICustom._allowed_reg_name).encode(charset)
        else:
            if len(original) - 1 > next_index and hasPort and original[next_index] == ':':  # not empty
                from_index = next_index + 1
                try:
                    self._port = int(original[from_index:])
                except ValueError as error:
                    raise Exception("invalid port number")
            # set a server-based naming authority
            buf = bytearray()
            if URICustom._userinfo is not None:  # has_userinfo
                buf.extend(URICustom._userinfo)
                buf.extend(b'@')
            if self._host is not None:
                buf.extend(URICustom._userinfo)
                if self._port != -1:
                    buf.extend(b':')
                    buf.extend(str(self._port).encode(charset))
            self._authority = bytes(buf)
            # Set flag
            self._is_server = True

    def _validate(self, component: list, generous: bitarray):
        return self._validate_helper(component, 0, -1, generous)

    def _validate_helper(self, component: list, s_offset: int, e_offset: int, generous: bitarray):
        if e_offset == -1:
            e_offset = len(component) - 1
        for i in range(s_offset, e_offset+1):
            if not generous.__getitem__(component[i]):
                return False
        return True

    def setURI(self):   # to be revised A LOT
        # Initialize a string buffer
        buf = []

        # Construct the URI
        # ^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?

        if self._scheme is not None:
            buf.append(self._scheme + ':')

        if self.is_net_path:
            buf.append('//')
            if self._authority is not None:
                buf.append(self._authority)

        if self._opaque is not None and self._is_opaque_part:
            buf.append(self._opaque)
        elif self._path is not None:
            # _is_hier_part or _is_relativeURI
            if len(self._path) != 0:
                buf.append(self._path)

        if self._query is not None:
            buf.append('?' + self._query)

        # Ignore the fragment identifier

        # Convert the constructed URI to a character array
        self._uri = list(''.join(buf))
        self.hash = 0  # Assuming hash is an instance variable

    # def _get_raw_path(self):
    #     return _opaque if _is_opaque_part else _path

    def index_first_of(self, s: str, delims: str, offset: int):
        if s is None or len(s) == 0:
            return -1
        if delims is None or len(delims) == 0:
            return -1
        if offset < 0:
            offset = 0
        elif offset > len(s):
            return -1
        mini: int = len(s)
        for i in range(len(delims)):
            at_idx = s.index(delims[i], offset)
            if mini > at_idx >= 0:
                mini = at_idx
        return -1 if mini == len(s) else mini

    def prevalidate(self, component: str, disallowed: bitarray):
        if component is None:
            return False  # undefined
        for i in range(len(component)):
            if disallowed.__getitem__(component[i]):
                return False
        return True

    def _remove_fragment_identifier(self, component):
        if component is None:
            return None
        last_index = component.index('#')
        if last_index != -1:
            component = component[:last_index]
        return component

    def set_raw_path(self, escaped_path: str):
        if escaped_path is None or len(escaped_path) == 0:
            self._path = self._opaque = escaped_path
            self.setURI()
            return
        escaped_path = self._remove_fragment_identifier(escaped_path)
        if self.is_net_path or self.is_abs_path:
            if not escaped_path[0] == '/':
                raise Exception("not absolute path")
            if not self._validate(escaped_path, URICustom._abs_path):
                raise Exception("escaped bsolute path not valid")
            self._path = escaped_path
        elif self.is_rel_path:
            at_idx = self.index_first_of(escaped_path, "/", 0)
            if at_idx == 0:
                raise Exception("incorrect path")
            if at_idx > 0 and not self._validate_helper(escaped_path, 0, at_idx-1, URICustom._rel_segment) and \
                not self._validate_helper(escaped_path, at_idx, -1, URICustom._abs_path) or \
                at_idx < 0 and not self._validate_helper(escaped_path, 0, -1, URICustom._rel_segment):
                raise Exception("escaped relative path not valid")
            self._path = escaped_path
        elif self._is_opaque_part:
            if not URICustom._uric_no_slash.__getitem__(escaped_path[0]) and not self._validate_helper(escaped_path, 1, -1, URICustom._uric):
                raise Exception("escaped opaque part not valid")
            self._opaque = escaped_path
        else:
            raise Exception("incorrect path")
        self.setURI()

    def set_path(self, path: str):
        if path is None or len(path) == 0:
            self._path = self._opaque = path
            self.setURI()
            return
        charset = self.get_protocol_charset()
        if self.is_net_path or self.is_abs_path:
            self._path = self.encode(path, URICustom._allowed_abs_path, charset)
        elif self.is_rel_path:
            pass  # to be continued later!


    def get_protocol_charset(self):
        if self.protocol_charset is not None:
            return self.protocol_charset
        return "UTF-8"

    def __getBytes(self, data, charset):
        if data is None:
            raise ValueError("data may not be null")
        if charset is None or len(charset) == 0:
            raise ValueError("charset may not be null or empty")
        try:
            return data.encode(charset)
        except LookupError:
            if self.LOG.isEnabledFor(logging.WARNING):
                self.LOG.warning("Unsupported encoding: {}. System encoding used.".format(charset))
            return data.encode()

    def encode(self, original: str, allowed: bitarray, charset: str):
        if original is None:
            raise Exception("original string may not be null")
        if allowed is None:
            raise Exception("allowed bitset may not be null")
        url_codec = URLCodec()
        rawdata = url_codec.encode_url(allowed, self.__getBytes(original, charset))
        return rawdata.decode('ascii')



def check():
    b = bitarray(256)
    b.setall(False)
    print(b)
    for i in range(48, 58, 1):
        b.__setitem__(i, True)
    print(b)


uri = URICustom()
# print(uri.ay7aga)
# print(URICustom._rel_segment)
# check()
