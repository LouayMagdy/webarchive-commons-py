from bitarray import bitarray
from urllib.parse import urlparse, urlunparse


class URI:
    hostname = None
    top_label = None
    alphanum = None
    alpha = None
    digit = None
    scheme = None

    def __init__(self, uri_string):
        self.uri = urlparse(uri_string)

    def getScheme(self):
        return self.uri.scheme

    def getAuthority(self):
        return self.uri.netloc

    def __str__(self):
        return urlunparse(self.uri)

    @classmethod
    def initialize(cls):
        cls.digit = bitarray(256)
        for i in range(48, 58, 1):
            cls.digit.__setitem__(i, True)

        cls.alpha = bitarray(256)
        for i in range(97, 123, 1):
            cls.alpha.__setitem__(i, True)
        for i in range(65, 91, 1):
            cls.alpha.__setitem__(i, True)

        cls.alphanum = bitarray(256)
        cls.alphanum.__or__(cls.alpha)
        cls.alphanum.__or__(cls.digit)

        cls.top_label = bitarray(256)
        cls.top_label.__or__(cls.alphanum)

        cls.hostname = bitarray(256)
        cls.hostname.__or__(cls.top_label)

        cls.scheme = bitarray(256)
        cls.scheme.__or__(cls.alpha)
        cls.scheme.__or__(cls.digit)
        cls.scheme.__setitem__(43, True)
        cls.scheme.__setitem__(45, True)
        cls.scheme.__setitem__(46, True)
