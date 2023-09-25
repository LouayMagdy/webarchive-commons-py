from bitarray import bitarray
from urllib.parse import urlparse, quote, urlsplit, urlunsplit, urlunparse
import urllib.parse
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

    return cls


@initialize
class URICustom:
    def __init__(self, s: str = None, strict: bool = False, charset: str = None):
        self._authority = None
        self.protocol_charset = charset
        self._uri = None
        self._is_opaque_part: bool = True
        self._opaque: list
        self.authority = None
        self._host = None
        self._is_reg_name: bool = False
        self._is_server: bool = False
        self._is_hostname: bool = False
        self._is_IPv4address: bool = False
        self._is_IPv6reference: bool = False
        self._port: int = -1

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


    # def _get_raw_path(self):
    #     return _opaque if _is_opaque_part else _path


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
