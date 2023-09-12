import re
from tld import get_tld
import tldextract


class URLRegexTransformer:
    def __init__(self):
        self.PATH_OPTS = [
            self.OptimizedPattern("(?i)^.*/(\\((?:[a-z]\\([0-9a-z]{24}\\))+\\)/)[^\\?]+\\.aspx.*$", ".aspx", 1, 1),
            self.OptimizedPattern("(?i)^.*/(\\([0-9a-z]{24}\\)/)(?:[^\\?]+\\.aspx.*)$", ".aspx", 1, 1)
        ]
        self.QUERY_OPTS = [
            self.OptimizedPattern("(?i)^(.*)(?:jsessionid=[0-9a-zA-Z]{32})(?:&(.*))?$", "jsessionid=", 1, 2),
            self.OptimizedPattern("(?i)^(.*)(?:phpsessid=[0-9a-zA-Z]{32})(?:&(.*))?$", "phpsessid=", 1, 2),
            self.OptimizedPattern("(?i)^(.*)(?:sid=[0-9a-zA-Z]{32})(?:&(.*))?$", "sid=", 1, 2),
            self.OptimizedPattern("(?i)^(.*)(?:ASPSESSIONID[a-zA-Z]{8}=[a-zA-Z]{24})(?:&(.*))?$", "aspsessionid", 1, 2),
            self.OptimizedPattern("(?i)^(.*)(?:cfid=[^&]+&cftoken=[^&]+)(?:&(.*))?$", "cftoken=", 1, 2),
        ]

    @staticmethod
    def strip_opts(orig: str, op):
        orig_LC = orig.lower()
        sb = ""
        i = 0
        maxi = len(op)
        while i < maxi:
            try:
                orig_idx = orig_LC.index(op[i].match)
            except:
                orig_idx = -1

            if orig_idx != -1:
                sb = orig
                break
            i += 1
        if sb == "":
            return orig

        while i < maxi:
            try:
                orig_idx = orig_LC.index(op[i].match)
            except:
                orig_idx = -1

            if orig_idx != -1:
                m = op[i].pattern.match(sb)
                if m is not None and m.matches():  # NOT SURE ABOUT THIS LINE
                    if m.group(op[i].end) is not None:
                        sb = sb[:m.end(op[i].start)] + sb[m.start(op[i].end):]
            i += 1
        return sb

    @staticmethod
    def strip_path_session_id(self, path):
        return self.strip_opts(path, self.PATH_OPTS)

    @staticmethod
    def strip_query_session_id(self, query):
        return self.strip_opts(query, self.QUERY_OPTS)

    class OptimizedPattern:
        def __init__(self, regex, match, start, end):
            self.pattern = re.compile(regex)
            self.match = match
            self.start = start
            self.end = end

        @staticmethod
        def host_to_public_suffix(host):
            try:
                idn = get_tld(host, fix_protocol=True, fail_silently=True)
            except:
                return host
            tmp = tldextract.extract(idn).suffix
            if tmp is None:
                return host
            pub_suff = str(tmp)
            idx = host.rfind(".", 0, len(host) - (len(pub_suff) + 2))
            if idx == -1:
                return host
            return host[idx + 1:]

        @staticmethod
        def host_to_surt(host):
            parts = host.split(".", -1)
            if len(parts) == 1:
                return host
            sb = ""
            for i in range(len(parts) - 1, 0, -1):
                sb += parts[i] + ","
            sb += parts[0]
            return sb
