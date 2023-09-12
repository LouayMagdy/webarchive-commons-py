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
                if m is not None:  # NOT SURE ABOUT THIS LINE
                    if op[i].start == op[i].end:
                        sb = sb[:m.start(op[i].start)] + sb[m.end(op[i].end):]
                    else:
                        if m.group(op[i].end) is None:
                            sb = sb[:m.end(op[i].start)]
                        else:
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








########################## TESTING ##########################
test = URLRegexTransformer()


# def test_stripPathSessionID():
#     # Check ASP_SESSIONID2:
#     check_stripPathSessionID(
#         "/(S(4hqa0555fwsecu455xqckv45))/mileg.aspx",
#         "/mileg.aspx"
#     )
#
#     # Check ASP_SESSIONID2 (again):
#     check_stripPathSessionID(
#         "/(4hqa0555fwsecu455xqckv45)/mileg.aspx",
#         "/mileg.aspx"
#     )
#
#     # Check ASP_SESSIONID3:
#     check_stripPathSessionID(
#         "/(a(4hqa0555fwsecu455xqckv45)S(4hqa0555fwsecu455xqckv45)f(4hqa0555fwsecu455xqckv45))/mileg.aspx?page=sessionschedules",
#         "/mileg.aspx?page=sessionschedules"
#     )
#
#     # '@' in path:
#     check_stripPathSessionID(
#         "/photos/36050182@N05/",
#         "/photos/36050182@N05/"
#     )
#
#
# def check_stripPathSessionID(orig, want):
#     got = test.strip_path_session_id(test, orig)
#     assert want == got, f"FAIL Orig({orig}) Got({got}) Want({want})"
#
#
# test_stripPathSessionID()


#############################################

# def test_SURT():
#     assert test.host_to_surt("www.archive.org") == "org,archive,www"
#
#
# test_SURT()


#############################################

# def test_strip_query_session_id():
#     BASE = ""
#     str32id = "0123456789abcdefghijklemopqrstuv"
#     url = BASE + "?jsessionid=" + str32id
#     expected_result = BASE + "?"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Test that we don't strip if not 32 chars only.
#     url = BASE + "?jsessionid=" + str32id + '0'
#     expected_result = url
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Test what happens when followed by another key/value pair.
#     url = BASE + "?jsessionid=" + str32id + "&x=y"
#     expected_result = BASE + "?x=y"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed (" + result + ")"
#
#     # Test what happens when followed by another key/value pair and
#     # prefixed by a key/value pair.
#     url = BASE + "?one=two&jsessionid=" + str32id + "&x=y"
#     expected_result = BASE + "?one=two&x=y"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Test what happens when prefixed by a key/value pair.
#     url = BASE + "?one=two&jsessionid=" + str32id
#     expected_result = BASE + "?one=two&"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Test aspsession.
#     url = BASE + "?aspsessionidABCDEFGH=" + "ABCDEFGHIJKLMNOPQRSTUVWX" + "&x=y"
#     expected_result = BASE + "?x=y"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Test archive phpsession.
#     url = BASE + "?phpsessid=" + str32id + "&x=y"
#     expected_result = BASE + "?x=y"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # With prefix too.
#     url = BASE + "?one=two&phpsessid=" + str32id + "&x=y"
#     expected_result = BASE + "?one=two&x=y"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # With only prefix
#     url = BASE + "?one=two&phpsessid=" + str32id
#     expected_result = BASE + "?one=two&"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Test sid.
#     url = BASE + "?" + "sid=9682993c8daa2c5497996114facdc805" + "&x=y"
#     expected_result = BASE + "?x=y"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     # Igor test.
#     url = BASE + "?" + "sid=9682993c8daa2c5497996114facdc805" + "&" + "jsessionid=" + str32id
#     expected_result = BASE + "?"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     url = "?CFID=1169580&CFTOKEN=48630702&dtstamp=22%2F08%2F2006%7C06%3A58%3A11"
#     expected_result = "?dtstamp=22%2F08%2F2006%7C06%3A58%3A11"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     url = "?CFID=12412453&CFTOKEN=15501799&dt=19_08_2006_22_39_28"
#     expected_result = "?dt=19_08_2006_22_39_28"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     url = "?CFID=14475712&CFTOKEN=2D89F5AF-3048-2957-DA4EE4B6B13661AB&r=468710288378&m=forgotten"
#     expected_result = "?r=468710288378&m=forgotten"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     url = "?CFID=16603925&CFTOKEN=2AE13EEE-3048-85B0-56CEDAAB0ACA44B8"
#     expected_result = "?"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#     url = "?CFID=4308017&CFTOKEN=63914124&requestID=200608200458360%2E39414378"
#     expected_result = "?requestID=200608200458360%2E39414378"
#     result = test.strip_query_session_id(test, url)
#     assert expected_result == result, "Failed " + result
#
#
# test_strip_query_session_id()
