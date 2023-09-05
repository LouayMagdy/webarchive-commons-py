import URLCanonicalizer, BasicURLCanonicalizer, IAURLCanonicalizer, AggressiveIACanonicalizerRules, HandyURL

class AggressiveIAURLCanonicalizer:
    def __init__(self):
        self.basic = BasicURLCanonicalizer.BasicURLCanonicalizer()
        self.ia = IAURLCanonicalizer(AggressiveIACanonicalizerRules.AggressiveIACanonicalizerRules())


    def canonicalize(self, url: HandyURL):
        self.basic.canonicalize(url)
        self.ia.canonicalize(url)

