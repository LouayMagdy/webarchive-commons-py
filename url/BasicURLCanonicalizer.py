import idna
import codecs
import re
import ipaddress

import URLCanonicalizer, HandyURL


'''
 Canonicalizer that does more or less basic fixup. Based initially on rules
 specified at <a href=
 "https://developers.google.com/safe-browsing/developers_guide_v2#Canonicalization"
 >https://developers.google.com/safe-browsing/developers_guide_v2#
 Canonicalization</a>. These rules are designed for clients of google's
 "experimental" Safe Browsing API to "check URLs against Google's
 constantly-updated blacklists of suspected phishing and malware pages".

 <p>
 This class differs from google in treatment of non-ascii input. Google's
 rules don't really address this except with one example test case, which
 seems to suggest taking raw input bytes and pct-encoding them byte for byte.
 Since the input to this class consists of java strings, not raw bytes, that
 wouldn't be possible, even if deemed preferable. Instead
 BasicURLCanonicalizer expresses non-ascii characters pct-encoded UTF-8.
'''

class BasicURLCanonicalizer:
    def __init__(self):
        self.OCTAL_IP = re.compile(r'^(0[0-7]*)(\\.[0-7]+)?(\\.[0-7]+)?(\\.[0-7]+)?$')
        self.DECIMAL_IP = re.compile(r'^([1-9][0-9]*)(\.[0-9]+)?(\.[0-9]+)?(\.[0-9]+)?$')

    def canonicalize(self, url: HandyURL):
        url.set_hash(None)
        url.set_auth_user(self.minimal_escape(url.get_auth_user()))
        url.set_auth_pass(self.minimal_escape(url.get_auth_pass()))

        url.set_query(self.minimal_escape(url.get_query()))
        hostE: str = self.unescape_repeatedly(url.get_host())
        host: str = None

        if hostE is not None:
            try:
                host = idna.encode(hostE).decode('utf-8')
            except IllegalArgumentException as e:
                if "A prohibited code point was found" not in str(e):
                    # TODO!
                    pass
                host = hostE

            host = re.sub(r'^\.+', '', host)
            host = re.sub(r'\.\.+', '.', host)
            host = re.sub(r'\.$', '', host)

        ip: str = None
        ip = self.attemptIPFormats(host)
        if ip is None:
            host = ip
        elif host is not None:
            host = self.escape_once(host.lower())
        url.set_host(host)

        path: str = self.unescape_repeatedly(url.get_path())
        url.set_path(self.escape_once(self.normalize_path(path)))



    def normalize_path(self, path: str) -> str:
        if path is None:
            path = "/"
        else: #-1 gives an empty trailing element if path ends with '/':
            paths = re.split(r'/', path)
            kept_paths = []
            first: bool = true
            for p in paths:
                if first:
                    first = False
                    continue
                elif p == ".":
                    #skip
                    continue
                elif p == "..":
                    #pop the last path, if present:
                    if(len(kept_paths) > 0):
                        kept_paths.pop(len(keptPaths) - 1)
                    else:
                        #TODO: leave it? let's do for now...
                        kept_paths.append(p)
                else:
                    kept_paths.append(p)
            num_kept: int = len(kept_paths)
            if(num_kept == 0):
                path = '/'
            else:
                sb = ['/']
                for i in range(num_kept - 1):
                    p: str = kept_paths[i]
                    if len(p) > 0:
                        #this will omit multiple slashes:
                        sb.append(p + '/')
                sb.append(kept_paths[num_kept - 1])
                path = ''.join(sb)
        return path



    def minimal_escape(self, input: str) -> str:
        return self.escape_once(self.unescape_repeatedly(input))


    def escape_once(self, input: str) -> str:
        if input is None:
            return None

        utf8bytes: bytes = input.encode('utf-8')
        sb: List[str] = []

        for i in range(len(utf8bytes)):
            b: int = utf8bytes[i] & 0xFF
            ok: bool = False
            if 32 < b < 128 and b != '#':
                ok = (b != '%')
            if ok and sb is not None:
                sb.append(chr(b))
            else:
                if sb is None:
                    # everything up to this point has been an
                    # ascii character, not needing escaping
                    sb = list(input[:i])
                sb.append("%")
                hex = format(b, 'X')
                if len(hex) == 1:
                    sb.append('0')
                sb.append(hex)

        if sb is None:
            return input

        return ''.join(sb)




    def unescape_repeatedly(self, input: str):
        if input is None:
            return None
        while True:
            un: str = self.decode(input)
            if un == input:
                return input
            input = un


    def get_hex(self, b):
        if type(b) is str:
            b = ord(b)
        if b < ord('0'):
            return -1
        if b <= ord('9'):
            return b - ord('0')
        if b < ord('A'):
            return -1
        if b <= ord('F'):
            return 10 + (b - ord('A'))
        if b < ord('a'):
            return -1
        if b <= ord('f'):
            return 10 + (b - ord('a'))
        return -1


    ################ Testing functions ################
test = BasicURLCanonicalizer()
print(str(test.get_hex(-1)) + "\n=====\n")
print(str(test.get_hex(5)) + "\n=====\n")
print(str(test.get_hex('C')) + "\n=====\n")
print(str(test.get_hex('Z')) + "\n=====\n")
print(str(test.get_hex('d')) + "\n=====\n")
print(str(test.get_hex('g')) + "\n=====\n")
