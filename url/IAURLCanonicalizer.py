import re
import os
from HandyURL import HandyURL
from CanonicalizerConstants import CanonicalizerConstants as consts
from CanonicalizeRules import CanonicalizeRules
from URLCanonicalizer import URLCanonicalizer
from URLRegexTransformer import URLRegexTransformer
from helping_functions.StringFieldExtractor import StringFieldExtractor

# def alpha_reorder_query(orig):
#     if orig is None:
#         return None
#     if len(orig) <= 1:
#         return orig
#     if not (("=" in orig) and ("&" in orig)):
#         return orig
#     args = orig.split("&")
#     args_dict = {}
#
#     for arg in args:
#         if arg == "":
#             continue
#         key, value = arg.split("=")
#         args_dict[key] = value
#
#     args_dict = dict(sorted(args_dict.items()))
#
#     sb = []
#     maxi = len(args_dict) - 1
#     i = 0
#     for key, value in args_dict.items():
#         sb.append(key)
#         sb.append('=')
#         sb.append(value)
#         if i < maxi:
#             sb.append('&')
#         i += 1
#     return "".join(sb)


class IAURLCanonicalizer(URLCanonicalizer, consts):
    def __init__(self, rules: CanonicalizeRules):
        self.rules: CanonicalizeRules = rules
        self.WWWN_PATTERN = re.compile("^www\\d*\\.")

    # Helper function
    def _strip_path_session_id(self, path):
        """Strip the path and session ID from a URL."""
        pattern = r"^https?://\w+/.*?"  # Match any URL
        opt_patterns = [
            (r"^https?://\w+/.+?\.aspx", r".aspx"),  # Strip path prefix
            (r"^https?://\w+/\(([0-9a-zA-Z_]+)\)", r"?")  # Strip session ID
        ]
        stripped_path = ""
        for opt_pattern in opt_patterns:
            match = re.search(opt_pattern[0], path)
            if match:
                stripped_path += match.group(opt_pattern[1]) + "#"
                break
        return stripped_path[:-1]  # Remove the "#" at the end

    # Helper function
    def _strip_query_session_id(self, query: str) -> str:
        # Define the regular expression patterns for session ID tokens
        pattern_list = [
            {'pattern': r'(?i)^.*?(?:jsessionid=([0-9a-zA-Z]{32}))(?:(&amp;)?$)', 'start': 1, 'end': 2},
            {'pattern': r'(?i)^.*?(?:phpsessid=([0-9a-zA-Z]{32}))(?:(&amp;)?$)', 'start': 1, 'end': 2},
            {'pattern': r'(?i)^.*?(?:sid=([0-9a-zA-Z]{32}))(?:(&amp;)?$)', 'start': 1, 'end': 2},
            {'pattern': r'(?i)^.*?(?:ASPSESSIONID ([a-zA-Z]{8})=(([a-zA-Z]{24}))(?:(&amp;)?$)', 'start': 1, 'end': 2},
            {'pattern': r'(?i)^.*?(?:cfid=([^&]+)&cftoken=([^&]+))(?:(&amp;)?$)', 'start': 1, 'end': 2},
        ]

        # Use the regular expressions to extract the session ID token from the query string
        matches = []
        for pattern in pattern_list:
            match = re.search(pattern['pattern'], query)
            if match:
                group = match.group(pattern['start'])
                if group:
                    # Remove the session ID token from the query string
                    query = query[:match.start()] + query[match.end():]
                    matches.append((pattern['start'], pattern['end'], group))
        return query

    def canonicalize(self, url: HandyURL):
        if url.get_opaque() is not None:
            return
        if self.rules.is_set(consts.SCHEME_SETTINGS, consts.SCHEME_LOWERCASE):
            if url.get_scheme() is not None:
                url.set_scheme(url.get_scheme().lower())
        if self.rules.is_set(consts.HOST_SETTINGS, consts.HOST_LOWERCASE):
            url.set_host(url.get_host().lower())
        if self.rules.is_set(consts.HOST_SETTINGS, consts.HOST_MASSAGE):
            url.set_host(self.massage_host(self, url.get_host()))

        if self.rules.is_set(consts.AUTH_SETTINGS, consts.AUTH_STRIP_USER):
            url.set_auth_user(None)
            url.set_auth_pass(None)
        elif self.rules.is_set(consts.AUTH_SETTINGS, consts.AUTH_STRIP_PASS):
            url.set_auth_pass(None)

        if self.rules.is_set(consts.PORT_SETTINGS, consts.PORT_STRIP_DEFAULT):
            default_port: int = self.get_default_port(url.get_scheme())
            if default_port == url.get_port():
                url.set_port(HandyURL.DEFAULT_PORT)

        path: str = url.get_path()
        if self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_STRIP_EMPTY) and path == "/":
            url.set_path(None)
        else:
            if self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_LOWERCASE):
                path = path.lower()
            if self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_STRIP_SESSION_ID):
                for_self = URLRegexTransformer()
                path = URLRegexTransformer.strip_path_session_id(for_self, path)

            if self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_STRIP_EMPTY):
                url.set_path(None)
            elif self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_STRIP_TRAILING_SLASH_UNLESS_EMPTY):
                if path.endswith('/') and len(path) > 1:
                    path = path[0:len(path) - 1]
            url.set_path(path)

        query: str = url.get_query()
        if query is not None:
            # we have a query... what to do with it?
            # 1st: remove unneeded:
            if self.rules.is_set(consts.QUERY_SETTINGS, consts.QUERY_STRIP_SESSION_ID):
                if not query == '':
                    for_self = URLRegexTransformer()
                    query = URLRegexTransformer.strip_query_session_id(for_self, query)
            # lower-case
            if self.rules.is_set(consts.QUERY_SETTINGS, consts.QUERY_LOWERCASE):
                query = query.lower()
            # re-order?
            if self.rules.is_set(consts.QUERY_SETTINGS, consts.QUERY_ALPHA_REORDER):
                query = self.alpha_reorder_query(query)
            if query == "":
                if self.rules.is_set(consts.QUERY_SETTINGS, consts.QUERY_STRIP_EMPTY):
                    query = None
            url.set_query(query)

    @staticmethod
    def alpha_reorder_query(orig):
        if orig is None:
            return None
        if len(orig) <= 1:
            return orig
        if not (("=" in orig) or ("&" in orig)):
            return orig
        args = orig.split("&")
        sfe = StringFieldExtractor('=', 1)
        args_list = []

        for arg in args:
            if arg == "":
                args_list.append(('', ''))
                continue
            key, value = sfe.split(arg)
            args_list.append((key, value))

        args_list = sorted(args_list, key=lambda x: (x[0], x[1]))

        sb = []
        maxi = len(args_list) - 1
        i = 0
        for key, value in args_list:
            if not key is None and not key == '':
                sb.append(key)
                if value is not None:
                    sb.append('=')
                    sb.append(value)
            if i < maxi:
                sb.append('&')
            i += 1
        return "".join(sb)

    @staticmethod
    def massage_host(self, host: str) -> str:
        while True:
            m = self.WWWN_PATTERN.search(host)
            if m:
                host = host[m.end():]
            else:
                break
        return host

    @staticmethod
    def get_default_port(scheme: str):
        lc_scheme = scheme.lower()
        if lc_scheme == "http":
            return 80
        elif lc_scheme == "https":
            return 443
        return 0


# test = IAURLCanonicalizer(CanonicalizeRules())
# testcases = [None, "", "a", "ab", "a=1", "ab=1", "&a=1", "a=1&b=1", "a=a&a=a", "a=a&a=b", "a=a&a=b&b=a&b=b"]
# expected = [None, "", "a", "ab", "a=1", "ab=1", "a=1&", "a=1&b=1", "a=a&a=a", "a=b&a=a", "b=b&a=b&b=a&a=a"]
# for i in range(len(testcases)):
#     print(str(testcases[i]) + " : " + str(test.alpha_reorder_query(testcases[i])) + " --> " + str(expected[i]))
#     if expected[i] == test.alpha_reorder_query(testcases[i]):
#         print("Correct\n=======")
#     else:
#         print("Wrong!!\n======")
