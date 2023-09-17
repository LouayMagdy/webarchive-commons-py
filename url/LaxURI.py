from urllib.parse import urlparse, urlunparse
from bitarray import bitarray
from URI import URI


class LaxURI(URI):  # in java: extends URI
    lax_rel_segment = bitarray(256)
    lax_rel_segment.setall(False)

    def __init__(self, uri_string):
        super().__init__(uri_string)
        self.serial_version_UID = 5273922211722239537
        self.HTTP_SCHEME = ['h', 't', 't', 'p']
        self.HTTPS_SCHEME = ['h', 't', 't', 'p', 's']

    rel_segment = bitarray()
    lax_rel_segment |= rel_segment
    lax_rel_segment[ord(':')] = True





############## TO BE CONTINUED WHEN I UNDERSTAND WHAT IT DOES! ######################




rel_segment = bitarray(256)
rel_segment[b'a'] = 1
rel_segment[b'b'] = 1
rel_segment[b'c'] = 1
rel_segment[b'd'] = 1

lax_rel_segment = bytearray(256)
lax_rel_segment[:] = rel_segment
lax_rel_segment[b':'] = 1

print(bool(lax_rel_segment[b'a']))
print(bool(lax_rel_segment[b'b']))
print(bool(lax_rel_segment[b'c']))
print(bool(lax_rel_segment[b'd']))
print(bool(lax_rel_segment[b':']))
print(bool(lax_rel_segment[b'e']))



