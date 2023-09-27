from abc import ABC
from GoogleURLCanonicalzier import GoogleURLCanonicalizer
from URLCanonicalizer import URLCanonicalizer
from DefaultIACanonicalizerRules import DefaultIACanonicalizerRules
from CanonicalizeRules import CanonicalizeRules
from IAURLCanonicalizer import IAURLCanonicalizer
from HandyURL import HandyURL


class NonMassagingIAURLCanonicalizer(URLCanonicalizer, ABC):
    google = GoogleURLCanonicalizer()
    nonMassagingRules = DefaultIACanonicalizerRules()
    can = CanonicalizeRules()
    nonMassagingRules.set_rule(can.HOST_SETTINGS, can.HOST_LOWERCASE)

    ia = IAURLCanonicalizer(nonMassagingRules)

    def canonicalize(self, url: HandyURL):
        self.google.canonicalize(url)
        self.ia.canonicalize(url)


