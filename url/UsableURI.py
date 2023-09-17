from LaxURI import LaxURI
import re
from urllib.parse import urlparse, urlunparse


class UsableURI(LaxURI):
    MAX_URL_LENGTH = 2083
    MASSAGEHOST_PATTERN = "^www\\d*\\."

    def __init__(self, uri=None, escaped=False, charset=None):
        super().__init__()

        # if base is not None and relative is not None:
        #     super().__init__(base, relative)
        #     self.normalize()


        if uri is not None:
            self.uri = urlparse(uri)
        self.cachedHost = None
        self.cachedEscapedURI = None
        self.cachedString = None
        self.cachedAuthorityMinusUserinfo = None
        self.surtForm = None
        if charset is not None:
            # Handle character encoding here if needed
            pass

    def resolve(self, uri, escaped=False, charset=None):
        base_uri = self.uri
        resolved_uri = urlparse(uri)
        if escaped and not resolved_uri.netloc:
            # Handle escaped URI here if needed
            pass
        return UsableURI(urlunparse(resolved_uri._replace(scheme=base_uri.scheme, netloc=base_uri.netloc, path=resolved_uri.path)))

    def equals(self, other):
        if isinstance(other, UsableURI):
            return str(self) == str(other)
        return False

    def getHostBasename(self):
        if self.getReferencedHost() is None:
            return None
        return re.sub(self.MASSAGEHOST_PATTERN, '', self.getReferencedHost())

    def toCustomString(self):
        if self.cachedString is None:
            self.cachedString = str(self.uri)
            self.coalesceUriStrings()
        return self.cachedString

    def __str__(self):
        return self.toCustomString()

    def toUnicodeHostString(self):
        if not self.uri.hostname:
            return str(self)
        return str(self.uri)

    def getEscapedURI(self):
        if self.cachedEscapedURI is None:
            self.cachedEscapedURI = str(self.uri)
            self.coalesceUriStrings()
        return self.cachedEscapedURI

    def coalesceUriStrings(self):
        if self.cachedString is not None and self.cachedEscapedURI is not None and len(self.cachedString) == len(self.cachedEscapedURI):
            self.cachedString = self.cachedEscapedURI

    def getHost(self):
        if self.cachedHost is None:
            self.cachedHost = self.uri.hostname
            self.coalesceHostAuthorityStrings()
        return self.cachedHost

    def getReferencedHost(self):
        referenced_host = self.getHost()
        if referenced_host is None and self.uri.scheme == 'dns':
            possible_host = self.uri.path
            if possible_host and re.match("[-_\\w\\.:]+", possible_host):
                referenced_host = possible_host
        return referenced_host

    def getSurtForm(self):
        if self.surtForm is None:
            # Implement SURT conversion here
            pass
        return self.surtForm

    def getAuthorityMinusUserinfo(self):
        if self.cachedAuthorityMinusUserinfo is None:
            tmp = self.uri.netloc
            if tmp and '@' in tmp:
                tmp = tmp.split('@', 1)[1]
            self.cachedAuthorityMinusUserinfo = tmp
            self.coalesceHostAuthorityStrings()
        return self.cachedAuthorityMinusUserinfo

    def length(self):
        return len(self.getEscapedURI())

    def charAt(self, index):
        return self.getEscapedURI()[index]

    def subSequence(self, start, end):
        return self.getEscapedURI()[start:end]

    def compareTo(self, other):
        return str(self).compare(other)

    @staticmethod
    def hasScheme(possible_url):
        for c in possible_url:
            if c == ':':
                return True
            if c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                break
        return False

    @staticmethod
    def parseFilename(path_or_uri):
        if UsableURI.hasScheme(path_or_uri):
            parts = urlparse(path_or_uri)
            path = parts.path
        else:
            path = path_or_uri
        return path.split('/')[-1]

    def writeObject(self, stream):
        stream.writeUTF(self.toCustomString())



# from LaxURI import LaxURI
#
#
# class UsableURI(LaxURI):
#     def __init__(self):
#         super().__init__()
#         self.serial_version_UID = -1277570889914647093
#         self.MAX_URL_LENGTH = 2083
#         self.MASSAGEHOST_PATTERN = "^www\\d*\\."
#         self._cached_host = None
#         self._cached_escaped_URI = None
#         self._cached_string = None
#         self._cached_authority_minus_user_info = None
#         self._surt_form = None
#         # LaxURI.hostname.setall('_')
#
#     @property
#     def cached_host(self):
#         return self._cached_host
#
#     @cached_host.setter
#     def cached_host(self, value):
#         self._cached_host = value
#
#     def has_scheme(self, possible_url: str) -> bool:
#         result: bool = False
#         for i in range(len(possible_url)):
#             c = possible_url[i]
#             if c == ':':
#                 result = True
#                 break
#             if self.scheme is not None and not self.scheme.get(c):
#                 break
#         return result






###################### Testing ######################


test = UsableURI(None)

# print(test.hasScheme("http://www.archive.org"))
# print(test.hasScheme("http:"))
# print(test.hasScheme("ht/tp://www.archive.org"))
# print(test.hasScheme("/tmp"))
#
# filename = "x.arc.gz"
# print(test.parseFilename("/tmp/one.two/" + filename))
# print(test.parseFilename("http://archive.org/tmp/one.two/" + filename))
# print(test.parseFilename("rsync://archive.org/tmp/one.two/" + filename))

# base = UsableURI("http://www.archive.org/a", True, "UTF-8")
# relative = UsableURI("//www.facebook.com/?href=http://www.archive.org/a", True, "UTF-8")
# print(relative.getScheme())
# print(relative.getAuthority())

# NOT WORKING TESTS
#
## test2 = UsableURI(None, False, None, base, relative)
## print(str(test2))
#
# END OF NOT WORKING TESTS


# NOT WORKING TESTS
#
# tests = ["http://xn--x-4ga.dk", "xn--x-4ga.dk", "http://user:pass@xn--x-4ga.dk:8080", "http://user@xn--x-4ga.dk:8080", "http://xn--x-4ga.dk/foo/bar?query=q", "http://127.0.0.1/foo/bar?query=q"]
# trues = ["http://øx.dk", "xn--x-4ga.dk", "http://user:pass@øx.dk:8080", "http://user@øx.dk:8080", "http://øx.dk/foo/bar?query=q", "http://127.0.0.1/foo/bar?query=q"]
#
##for i in range(len(tests)):
##    result = str(UsableURI(tests[i], True, 'UTF-8').toUnicodeHostString())
##    print(result)
##    if not result == trues[i]:
##        print("Error: " + tests[i] + " should be " + trues[i])
##    print("===============")
#
# END OF NOT WORKING TESTS





