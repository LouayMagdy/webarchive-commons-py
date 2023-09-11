import BasicURLCanonicalizer, IAURLCanonicalizer, AggressiveIACanonicalizerRules, HandyURL
from URLCanonicalizer import URLCanonicalizer


class AggressiveIAURLCanonicalizer(URLCanonicalizer):
    def __init__(self):
        self.basic = BasicURLCanonicalizer.BasicURLCanonicalizer()
        self.ia = IAURLCanonicalizer(AggressiveIACanonicalizerRules.AggressiveIACanonicalizerRules())

    def canonicalize(self, url: HandyURL):
        self.basic.canonicalize(url)
        self.ia.canonicalize(url)

