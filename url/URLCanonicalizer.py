import HandyURL
from abc import ABC, abstractmethod


class URLCanonicalizer(ABC):
    @abstractmethod
    def canonicalize(self, url: HandyURL):  # to implement HandyURL
        pass
