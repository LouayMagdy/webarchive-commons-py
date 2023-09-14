from urllib.parse import urlparse, urlunparse
from bitarray import bitarray
from URI import URI


class LaxURI(URI):  # in java: extends URI
    def __init__(self):
        self.serial_version_UID = 5273922211722239537
        self.HTTP_SCHEME = ['h', 't', 't', 'p']
        self.HTTPS_SCHEME = ['h', 't', 't', 'p', 's']

        self.lax_rel_segment = bitarray(256)
        self.lax_rel_segment.setall(False)

############## TO BE CONTINUED WHEN I UNDERSTAND WHAT IT DOES! ######################






