import AggressiveIACanonicalizerRules
import BasicURLCanonicalizer
import HandyURL
import IAURLCanonicalizer
from URLCanonicalizer import URLCanonicalizer


class AggressiveIAURLCanonicalizer(URLCanonicalizer):
    def __init__(self):
        self.basic = BasicURLCanonicalizer.BasicURLCanonicalizer()
        self.ia = IAURLCanonicalizer.IAURLCanonicalizer(AggressiveIACanonicalizerRules.AggressiveIACanonicalizerRules())

    def canonicalize(self, url: HandyURL):
        self.basic.canonicalize(url)
        self.ia.canonicalize(url)

