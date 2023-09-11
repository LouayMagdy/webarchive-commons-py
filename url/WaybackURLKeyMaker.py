import urllib.parse
from urllib.parse import urlparse
from typing import List
from RewriteRule import RewriteRule
from DefaultIAURLCanonicalizer import DefaultIAURLCanonicalizer
from URLCanonicalizer import URLCanonicalizer
from URLRegexTransformer import URLRegexTransformer
from URLParser import URLParser


class WaybackURLKeyMaker:
    def __init__(self, surt_mode: bool = True):
        self.canonicalizer = DefaultIAURLCanonicalizer()
        self.surt_mode = surt_mode
        self.custom_rules = None

    def get_canonicalizer(self):
        return self.canonicalizer

    def set_canonicalizer(self, canonicalizer: URLCanonicalizer):
        self.canonicalizer = canonicalizer

    def is_surt_mode(self) -> bool:
        return self.surt_mode

    def make_key(self, url: str) -> str:
        if url is None:
            return "-"
        if len(url) == 0:
            return "-"
        if url.startswith("filedesc"):
            return url
        if url.startswith("warcinfo"):
            return url
        if url.startswith("dns:"):
            authority = url[4:]
            if not self.surt_mode:
                return authority
            surt = URLRegexTransformer.OptimizedPattern.host_to_surt(authority)
            return surt + ")"

        for_self = URLParser()
        hURL = URLParser.parse(for_self, url)  # NOT SURE AT ALL
        self.canonicalizer.canonicalize(hURL)
        key = hURL.get_url_string(self.surt_mode, self.surt_mode, False)
        if not self.surt_mode:
            return key
        parenIdx = key.index('(')
        if parenIdx == -1:
            return url
        key = key[parenIdx + 1:]
        if self.custom_rules is not None:
            key = self.apply_custom_rules(key)
        return key

    def get_custom_rules(self) -> List[RewriteRule]:
        return self.custom_rules

    def set_custom_rules(self, custom_rules: List[RewriteRule]) -> None:
        self.custom_rules = custom_rules

    def apply_custom_rules(self, urlkey: str) -> str:
        sb = urlkey
        for rule in self.custom_rules:
            rule.rewrite(sb)
        return sb
