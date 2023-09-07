import idna
import codecs
import re
import ipaddress
import socket

import URLCanonicalizer
from HandyURL import HandyURL

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
        self._UTF8 = None

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
            except Exception as e:
                if "A prohibited code point was found" not in str(e):
                    # TODO!
                    pass
                host = hostE

            host = re.sub(r'^\.+', '', host)
            host = re.sub(r'\.\.+', '.', host)
            host = re.sub(r'\.$', '', host)

        ip: str = None
        ip = self.attempt_IP_formats(host)
        if ip is not None:
            host = ip
        elif host is not None:
            host = self.escape_once(host.lower())
        url.set_host(host)

        path: str = self.unescape_repeatedly(url.get_path())
        url.set_path(self.escape_once(self.normalize_path(path)))

    def normalize_path(self, path: str) -> str:
        if path is None:
            path = "/"
        else:  # -1 gives an empty trailing element if path ends with '/':
            paths = re.split(r'/', path)
            kept_paths = []
            first: bool = True
            for p in paths:
                if first:
                    first = False
                    continue
                elif p == ".":
                    # skip
                    continue
                elif p == "..":
                    # pop the last path, if present:
                    if (len(kept_paths) > 0):
                        kept_paths.pop(len(kept_paths) - 1)
                    else:
                        # TODO: leave it? let's do for now...
                        kept_paths.append(p)
                else:
                    kept_paths.append(p)
            num_kept: int = len(kept_paths)
            if (num_kept == 0):
                path = '/'
            else:
                sb = ['/']
                for i in range(num_kept - 1):
                    p: str = kept_paths[i]
                    if len(p) > 0:
                        # this will omit multiple slashes:
                        sb.append(p + '/')
                sb.append(kept_paths[num_kept - 1])
                path = ''.join(sb)
        return path

    def attempt_IP_formats(self, host: str) -> str:
        if host is None:
            return None
        if re.match("^\\d+$", host):
            try:
                # Convert the integer into an IP address string
                host_int = int(host)
                return socket.inet_ntoa(host_int.to_bytes(4, byteorder='big'))

            except Exception as e:
                pass
        else:
            octal_pattern = r'^(0[0-7]*)(\.[0-7]+)?(\.[0-7]+)?(\.[0-7]+)?$'
            # matches = re.findall(octal_pattern, host)
            matches = host.split('.')
            if re.match(octal_pattern, host):
                parts: int = len(matches)
                if parts > 4:  # WHAT TO DO?
                    return None  # throw new URIException("Bad Host("+host+")");
                ip = [0] * 4
                for i in range(parts):
                    octet: int = 0
                    try:
                        # octet = int(matches[i][(0 if i == 0 else 1):], 8) # (((This line needs LOTS of revision)))
                        octet = int(matches[i], 8)
                    except Exception as e:
                        return None
                    if octet < 0 or octet > 255:
                        return None  # // throw new URIException("Bad Host("+host+")");
                    ip[i] = octet
                return f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'
            else:
                decimal_pattern = r'^([1-9][0-9]*)(\.[0-9]+)?(\.[0-9]+)?(\.[0-9]+)?$'
                # matches = re.findall(decimal_pattern, host)
                matches = host.split('.')
                if re.match(decimal_pattern, host):
                    parts: int = len(matches)
                    if parts > 4:  # WHAT TO DO?
                        return None
                        # throw new URIException("Bad Host("+host+")")
                    ip = [0] * 4
                    for i in range(parts):
                        m2_group: str = matches[i]
                        if m2_group is None:
                            return None
                        # // int octet =
                        # // Integer.parseInt(m2.group(i+1).substring((i==0)?0:1));
                        octet: int = 0
                        try:
                            # octet = int(m2_group[0 if i == 0 else 1:])
                            octet = int(m2_group)
                        except Exception as e:
                            return None
                        if octet < 0 or octet > 255:
                            return None  # // throw new URIException("Bad Host("+host+")");
                        ip[i] = octet
                    return f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'
        return None

    def UTF8(self):
        if self._UTF8 is None:
            self._UTF8 = codecs.lookup("utf-8")
        return self._UTF8

    def minimal_escape(self, input: str) -> str:
        return self.escape_once(self.unescape_repeatedly(input))

    def escape_once(self, input: str) -> str:
        if input is None:
            return None

        utf8bytes = input.encode('utf-8')
        sb: list[str] = []

        for i in range(len(utf8bytes)):
            b: int = utf8bytes[i] & 0xFF
            ok: bool = False
            if 32 < b < 128:
                if b != '#':
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

    def decode(self, input: str) -> str:
        sb = []
        pct_utf8_seq_start: int = -1
        bbuf = bytearray()  # Byte Buffer
        utf8decoder = None
        i: int = 0
        while i < len(input):
            # print("i=" + str(i) + " - input.length()=" + str(len(input)))
            c = input[i]
            h1, h2 = None, None
            if i <= len(input) - 3 and c == '%' and self.get_hex(input[i + 1]) >= 0 and self.get_hex(input[i + 2]) >= 0:
                h1 = self.get_hex(input[i + 1])
                h2 = self.get_hex(input[i + 2])
                if len(sb) == 0:  # // sb==null
                    if i > 0:
                        sb.append(input[0:i])
                b: int = ((h1 << 4) + h2) & 0xff
                if pct_utf8_seq_start < 0 and b < 0x80:
                    sb.append(chr(b))
                else:
                    if pct_utf8_seq_start < 0:
                        pct_utf8_seq_start = i
                        if bbuf is None:
                            bbuf = bytearray((len(input) - i) // 3)
                    bbuf.append(b)
                i += 3
            else:
                if pct_utf8_seq_start >= 0:
                    if utf8decoder is None:
                        utf8decoder = codecs.getdecoder("utf-8")  # // instead of UTF8().newDecoder()
                    self.append_decoded_pct_utf8(sb, bbuf, input, pct_utf8_seq_start, i, utf8decoder)
                    pct_utf8_seq_start = -1
                    bbuf.clear()
                if sb is not None:
                    sb.append(c)
                i += 1
        if pct_utf8_seq_start >= 0:
            if utf8decoder is None:
                utf8decoder = codecs.getdecoder("utf-8")
            self.append_decoded_pct_utf8(sb, bbuf, input, pct_utf8_seq_start, i, utf8decoder)

        if sb is not None:
            return ''.join(sb)
        else:
            return input

    ############ append_decoded_pct_utf8 function needs a lot of built-in modules to be implemented here (in python) ##############
    ############ WILL BE HANDLED LATER #############

    def append_decoded_pct_utf8(self, sb: [], bbuf, input: str, seq_start: int, seq_end: int, utf8decoder):
        #     # // assert bbuf.position() * 3 == seqEnd - seqStart;
        #     # assert bbuf.position() * 3 == seq_end - seq_start
        #
        #     utf8decoder.reset()
        #     cbuf = bytearray(bbuf.position())
        #     bbuf.flip()
        #
        #     while bbuf.position() < bbuf.limit():
        #         coder_result, _, _ = utf8decoder.decode(bbuf, cbuf, True)
        #         sb.append(cbuf.decode())
        #
        #         if coder_result.is_malformed():
        #             undecodable_pct_hex = input[seq_start + 3 * bbuf.position():
        #                                             seq_start + 3 * bbuf.position() + 3 * len(coder_result)]
        #             sb.append(undecodable_pct_hex)
        #             bbuf.position(bbuf.position() + len(coder_result))
        #
        #         cbuf.clear()
        pass

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
# print(str(test.get_hex(-1)) + "\n=====\n")
# print(str(test.get_hex(5)) + "\n=====\n")
# print(str(test.get_hex('C')) + "\n=====\n")
# print(str(test.get_hex('Z')) + "\n=====\n")
# print(str(test.get_hex('d')) + "\n=====\n")
# print(str(test.get_hex('g')) + "\n=====\n")


# print(str(test.normalize_path("/a/../b/c/./d")) + "\n=====\n")
# print(str(test.normalize_path("//my//folder///path")) + "\n=====\n")
# print(str(test.normalize_path("/my/folder/./path")) + "\n=====\n")
# print(str(test.normalize_path("/my/folder/../path")) + "\n=====\n")
# print(str(test.normalize_path("")) + "\n=====\n")
# print(str(test.normalize_path(None)) + "\n=====\n")


##################### NOT WORKING!!!! ######################
# print(str(test.attempt_IP_formats("192.168.0.1")) + "\n=====\n")
# print(str(test.attempt_IP_formats("0330.0250.0000.01")) + "\n=====\n")
# print(str(test.attempt_IP_formats("123456")) + "\n=====\n")
# print(str(test.attempt_IP_formats("0448.0250.0000.01")) + "\n=====\n")
# print(str(test.attempt_IP_formats("256.168.0.1")) + "\n=====\n")
# print(str(test.attempt_IP_formats("")) + "\n=====\n")
# print(str(test.attempt_IP_formats(None)))


# print(test.unescape_repeatedly("Hello World!") + "\n======")
# print(test.unescape_repeatedly("Hello & Goodbye") + "\n======")
# print(test.unescape_repeatedly("Hello # World!") + "\n======")
# print(test.unescape_repeatedly("Hello % World!") + "\n======")
# print(test.unescape_repeatedly("こんにちは") + "\n======")
# print(test.unescape_repeatedly("") + "\n======")
# print(str(test.unescape_repeatedly(None)) + "\n======")
# print(test.unescape_repeatedly("This is a very long input string that exceeds the typical length of a regular string") + "\n======")
# print(test.unescape_repeatedly("# % ! @") + "\n======")

# print(test.minimal_escape("Hello World!") + "\n======")
# print(test.minimal_escape("Hello & Goodbye") + "\n======")
# print(test.minimal_escape("Hello # World!") + "\n======")
# print(test.minimal_escape("Hello % World!") + "\n======")
# print(test.minimal_escape("こんにちは") + "\n======")
# print(test.minimal_escape("") + "\n======")
# print(str(test.minimal_escape(None)) + "\n======")
# print(test.minimal_escape("This is a very long input string that exceeds the typical length of a regular string") + "\n======")
# print(test.minimal_escape("# % ! @") + "\n======")


# print(test.decode("Hello%20World!") + "\n======")
# print(test.decode("Hello%20%3C%21%2D%2D%20World%20%2D%2D%3E") + "\n======")
# print(test.decode("Hello World!") + "\n======")
# print(test.decode("Hello%ZZWorld") + "\n======")
# print(test.decode("One % sign.") + "\n======")
# print(test.decode("H%65%6C%6C%6F %57o%72%6Cd!") + "\n======")
# print(test.decode("Hello%ZZ%20World") + "\n======")

handy_test = HandyURL("http", "user", "pass", "www.example.com", 8080, "/path", "param=value", "fragment")
print(handy_test.get_url_string())
test.canonicalize(handy_test)
print(handy_test.get_url_string())

print("================")

handy_test = HandyURL()
handy_test.set_scheme("http")
handy_test.set_host("www.example.com")
print(handy_test.get_url_string())
test.canonicalize(handy_test)
print(handy_test.get_url_string())

print("================")




