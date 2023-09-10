# import urllib.parse
# from urllib.parse import urlparse
# from typing import List
# from RewriteRule import RewriteRule
# from DefaultIAURLCanonicalizer import DefaultIAURLCanonicalizer
#
# 
# class WaybackURLKeyMaker:
#     def __init__(self):
#         self.canonicalizer = DefaultIAURLCanonicalizer()
#         self.surtMode = True
#         self.customRules = None
#
#     def make_key(self, url: str) -> str:
#         if url.startswith("dns:"):
#             authority = url[4:]
#             if not self.surtMode:
#                 return authority
#             surt = URLRegexTransformer.hostToSURT(authority)
#             return surt + ")"
#
#         hURL = URLParser.parse(url)
#         self.canonicalizer.canonicalize(hURL)
#         key = hURL.getURLString(self.surtMode, self.surtMode, False)
#         if not self.surtMode:
#             return key
#         parenIdx = key.index('(')
#         if parenIdx == -1:
#             return url
#         key = key[parenIdx + 1:]
#         if self.customRules is not None:
#             key = self.applyCustomRules(key)
#         return key
#
#     def getCustomRules(self) -> List[RewriteRule]:
#         return self.customRules
#
#     def setCustomRules(self, customRules: List[RewriteRule]) -> None:
#         self.customRules = customRules
#
#     def applyCustomRules(self, urlkey: str) -> str:
#         sb = StringBuilder(urlkey)
#         for rule in self.customRules:
#             rule.rewrite(sb)
#         return sb.toString()
