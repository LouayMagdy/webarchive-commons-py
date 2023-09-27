import re
from HandyURL import HandyURL
import urllib.parse


class URLParser:
    """
     * RFC 2396-inspired regex.
     *
     * From the RFC Appendix B:
     * <pre>
     * URI Generic Syntax                August 1998
     *
     * B. Parsing a URI Reference with a Regular Expression
     *
     * As described in Section 4.3, the generic URI syntax is not sufficient
     * to disambiguate the components of some forms of URI.  Since the
     * "greedy algorithm" described in that section is identical to the
     * disambiguation method used by POSIX regular expressions, it is
     * natural and commonplace to use a regular expression for parsing the
     * potential four components and fragment identifier of a URI reference.
     *
     * The following line is the regular expression for breaking-down a URI
     * reference into its components.
     *
     * ^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?
     *  12            3  4          5       6  7        8 9
     *
     * The numbers in the second line above are only to assist readability;
     * they indicate the reference points for each subexpression (i.e., each
     * paired parenthesis).  We refer to the value matched for subexpression
     * <n> as $<n>.  For example, matching the above expression to
     *
     * http://www.ics.uci.edu/pub/ietf/uri/#Related
     *
     * results in the following subexpression matches:
     *
     * $1 = http:
     * $2 = http
     * $3 = //www.ics.uci.edu
     * $4 = www.ics.uci.edu
     * $5 = /pub/ietf/uri/
     * $6 = <undefined>
     * $7 = <undefined>
     * $8 = #Related
     * $9 = Related
     *
     * where <undefined> indicates that the component is not present, as is
     * the case for the query component in the above example.  Therefore, we
     * can determine the value of the four components and fragment as
     *
     * scheme    = $2
     * authority = $4
     * path      = $5
     * query     = $7
     * fragment  = $9
     * </pre>
     *
     * --
     * <p>Below differs from the rfc regex in that...
     * (1) it has java escaping of regex characters
     * (2) we allow a URI made of a fragment only (Added extra
     * group so indexing is off by one after scheme).
     * (3) scheme is limited to legal scheme characters
    """
    def __init__(self):
        self.RFC2396REGEX = (
            re.compile("^(([a-zA-Z][a-zA-Z0-9\\+\\-\\.]*):)?((//([^/?#]*))?([^?#]*)(\\?([^#]*))?)?(#(.*))?"))
        self.COMMERCIAL_AT = '@'
        self.PERCENT_SIGN = '%'
        self.COLON = ':'
        self.STRAY_SPACING = "[\n|\r|\t]*"
        self.HTTP_SCHEME_SLASHES = re.compile("^(https?://)/+(.*)")
        self.DNS_SCHEME = "dns:"
        self.FILEDESC_SCHEME = "filedesc:"
        self.WARCINFO_SCHEME = "warcinfo:"
        self.HTTP_SCHEME = "http://"
        self.HTTPS_SCHEME = "https://"
        self.FTP_SCHEME = "ftp://"
        self.MMS_SCHEME = "mms://"
        self.RTSP_SCHEME = "rtsp://"
        self.DEFAULT_SCHEME = self.HTTP_SCHEME
        self.WAIS_SCHEME = "wais://"
        self.ALL_SCHEMES = [
            self.HTTP_SCHEME,
            self.HTTPS_SCHEME,
            self.FTP_SCHEME,
            self.MMS_SCHEME,
            self.RTSP_SCHEME,
            self.WAIS_SCHEME
        ]
        self.ALL_SCHEMES_PATTERN = re.compile("(?i)^(http|https|ftp|mms|rtsp|wais)://.*")

    @staticmethod
    def url_to_scheme(self, url: str) -> str:
        for scheme in self.ALL_SCHEMES:
            if url.startswith(scheme):
                return scheme
        return None

    @staticmethod
    def add_default_scheme_if_needed(self, url_string: str) -> str:
        if url_string is None:
            return None
        m2 = re.match(self.ALL_SCHEMES_PATTERN, url_string)
        if m2:
            return url_string
        return self.DEFAULT_SCHEME + url_string

    @staticmethod
    def parse(self, url_string: str) -> HandyURL:
        url_string = url_string.strip()
        url_string = url_string.replace(self.STRAY_SPACING, "")
        # regex doesn't work with the \r if it is in the middle of a word (with no spaces around), so I explicitely wrote it!
        url_string = url_string.replace('\r', '')
        url_string = url_string.replace('\n', '')
        url_string = url_string.replace('\t', '')
        if url_string.startswith(self.DNS_SCHEME) or url_string.startswith(self.FILEDESC_SCHEME) or url_string.startswith(self.WARCINFO_SCHEME):
            h = HandyURL()
            h.set_opaque(url_string)
            return h
        url_string = URLParser.add_default_scheme_if_needed(self, url_string)
        m1 = self.HTTP_SCHEME_SLASHES.match(url_string)
        if m1:
            url_string = m1.group(1) + m1.group(2)
        matcher = self.RFC2396REGEX.match(url_string)
        if not matcher:
            raise ValueError(f"{url_string}: string does not match RFC 2396 regex")
        uri_scheme = matcher.group(2)
        uri_authority = matcher.group(5)
        uri_path = matcher.group(6)
        uri_query = matcher.group(8)
        uri_fragment = matcher.group(10)

        user_name = None
        user_pass = None
        hostname = None
        port: int = HandyURL.DEFAULT_PORT
        user_info = None
        colon_port = None

        try:
            at_index = uri_authority.index(self.COMMERCIAL_AT)
        except:
            at_index = -1  # return -1 if not found

        try:
            port_colon_index = uri_authority.index(self.COLON, 0 if at_index < 0 else at_index)
        except:
            port_colon_index = -1  # return -1 if not found

        if at_index < 0 and port_colon_index < 0:
            hostname = uri_authority
        elif at_index < 0 and port_colon_index > -1:
            hostname = uri_authority[:port_colon_index]
            colon_port = uri_authority[port_colon_index:]
        elif at_index > -1 and port_colon_index < 0:
            user_info = uri_authority[:at_index]
            hostname = uri_authority[at_index + 1:]
        else:
            user_info = uri_authority[:at_index]
            hostname = uri_authority[at_index + 1:port_colon_index]
            colon_port = uri_authority[port_colon_index:]
        if colon_port is not None:
            if colon_port.startswith(self.COLON):
                if not len(colon_port) == 1:
                    try:
                        port = int(colon_port[1:])
                    except SyntaxError:
                        raise SyntaxError(f"{url_string}: bad port {colon_port[1:]}")
            else:
                # What's happened?!
                pass
        if user_info is not None:
            try:
                pass_colon_index = user_info.index(self.COLON)
            except:
                pass_colon_index = -1
            if pass_colon_index == -1:  # no password
                user_name = user_info
            else:
                user_name = user_info[:pass_colon_index]
                user_pass = user_info[pass_colon_index + 1:]
        return HandyURL(uri_scheme, user_name, user_pass, hostname, port, uri_path, uri_query, uri_fragment)







######################## Testing ########################

# test = URLParser()
#
#
# def add_default_scheme_if_needed_test():
#     print(URLParser.add_default_scheme_if_needed(test, None))
#     print(URLParser.add_default_scheme_if_needed(test, ""))
#     print(URLParser.add_default_scheme_if_needed(test, "http://www.fool.com"))
#     print(URLParser.add_default_scheme_if_needed(test, "http://www.fool.com/"))
#     print(URLParser.add_default_scheme_if_needed(test, "www.fool.com"))
#     print(URLParser.add_default_scheme_if_needed(test, "www.fool.com/"))
#
#     # assert URLParser.add_default_scheme_if_needed(test, None) is None
#     # assert URLParser.add_default_scheme_if_needed(test, "") == "http://"
#     # assert URLParser.add_default_scheme_if_needed(test, "http://www.fool.com") == "http://www.fool.com"
#     # assert URLParser.add_default_scheme_if_needed(test, "http://www.fool.com/") == "http://www.fool.com/"
#     # assert URLParser.add_default_scheme_if_needed(test, "www.fool.com") == "http://www.fool.com"
#     # assert URLParser.add_default_scheme_if_needed(test, "www.fool.com/") == "http://www.fool.com/"
#     # print("Test_add_default_scheme_if_needed passed!!")
#
#
# add_default_scheme_if_needed_test()
#
#
# def parse_test():
#     print("O(%s) E(%s)" % ("%66", urllib.parse.unquote("%66")))
#
#     check_parse("http://www.archive.org/index.html#foo", None, "http", None, None, "www.archive.org", -1, "/index.html", None, "foo", "http://www.archive.org/index.html#foo", "/index.html")
#     check_parse("http://www.archive.org/", None, "http", None, None, "www.archive.org", -1, "/", None, None, "http://www.archive.org/", "/")
#     check_parse("http://www.archive.org", None, "http", None, None, "www.archive.org", -1, "", None, None, "http://www.archive.org", "")
#     check_parse("http://www.archive.org?", None, "http", None, None, "www.archive.org", -1, "", "", None, "http://www.archive.org/?", "/?")
#     check_parse("http://www.archive.org#", None, "http", None, None, "www.archive.org", -1, "", None, "", "http://www.archive.org/#", "/")
#     check_parse("http://www.archive.org#foo#bar#baz", None, "http", None, None, "www.archive.org", -1, "", None, "foo#bar#baz", "http://www.archive.org/#foo#bar#baz", "/")
#     check_parse("http://www.archive.org:8080/index.html?query#foo", None, "http", None, None, "www.archive.org", 8080, "/index.html", "query", "foo", "http://www.archive.org:8080/index.html?query#foo", "/index.html?query")
#     check_parse("http://www.archive.org:8080/index.html?#foo", None, "http", None, None, "www.archive.org", 8080, "/index.html", "", "foo", "http://www.archive.org:8080/index.html?#foo", "/index.html?")
#     check_parse("http://www.archive.org:8080?#foo", None, "http", None, None, "www.archive.org", 8080, "", "", "foo", "http://www.archive.org:8080/?#foo", "/?")
#     check_parse("http://bücher.ch:8080?#foo", None, "http", None, None, "bücher.ch", 8080, "", "", "foo", "http://bücher.ch:8080/?#foo", "/?")
#
#     check_parse("dns:bücher.ch", "dns:bücher.ch", None, None, None, None, -1, None, None, None, "dns:bücher.ch", "")
#
#     check_parse("http://www.archive.org/?foo?what", None, "http", None, None, "www.archive.org", -1, "/", "foo?what", None, "http://www.archive.org/?foo?what", "/?foo?what")
#     check_parse("http://www.archive.org/?foo?what#spuz?baz?", None, "http", None, None, "www.archive.org", -1, "/", "foo?what", "spuz?baz?", "http://www.archive.org/?foo?what#spuz?baz?", "/?foo?what")
#     check_parse("http://www.archive.org/?foo?what#spuz?baz?#fooo", None, "http", None, None, "www.archive.org", -1, "/", "foo?what", "spuz?baz?#fooo", "http://www.archive.org/?foo?what#spuz?baz?#fooo", "/?foo?what")
#     check_parse("http://jdoe@www.archive.org:8080/index.html?query#foo", None, "http", "jdoe", None, "www.archive.org", 8080, "/index.html", "query", "foo", "http://jdoe@www.archive.org:8080/index.html?query#foo", "/index.html?query")
#     check_parse("http://jdoe:****@www.archive.org:8080/index.html?query#foo", None, "http", "jdoe", "****", "www.archive.org", 8080, "/index.html", "query", "foo", "http://jdoe:****@www.archive.org:8080/index.html?query#foo", "/index.html?query")
#     check_parse("http://:****@www.archive.org:8080/index.html?query#foo", None, "http", "", "****", "www.archive.org", 8080, "/index.html", "query", "foo", "http://:****@www.archive.org:8080/index.html?query#foo", "/index.html?query")
#     check_parse(" \n http://:****@www.archive.org:8080/inde\rx.html?query#foo \r\n \t ", None, "http", "", "****", "www.archive.org", 8080, "/index.html", "query", "foo", "http://:****@www.archive.org:8080/index.html?query#foo", "/index.html?query")
#     print("done checking!")
#     # print("done checking!")
#
#
# def check_parse(s, opaque, scheme, authUser, authPass, host, port, path, query, fragment, urlString, pathQuery):
#     h = URLParser.parse(test, s)
#
#     # print("Input:(%s)" % s)
#     # print("HandyURL\t%s" % h.to_debug_string())
#
#     # assert scheme == h.get_scheme()
#     if not scheme == h.get_scheme():
#         print("Scheme mismatch: %s != %s" % (scheme, h.get_scheme()))
#
#     # assert authUser == h.get_auth_user()
#     if not authUser == h.get_auth_user():
#         print("authUser mismatch: %s != %s" % (authUser, h.get_auth_user()))
#
#     # assert authPass == h.get_auth_pass()
#     if not authPass == h.get_auth_pass():
#         print("authPass mismatch: %s != %s" % (authPass, h.get_auth_pass()))
#
#     # assert host == h.get_host()
#     if not host == h.get_host():
#         print("host mismatch: %s != %s" % (host, h.get_host()))
#
#     # assert port == h.get_port()
#     if not port == h.get_port():
#         print("port mismatch: %s != %s" % (port, h.get_port()))
#
#     # assert path == h.get_path()
#     if not path == h.get_path():
#         print("path mismatch: %s != %s" % (path, h.get_path()))
#
#     # assert query == h.get_query()
#     if not query == h.get_query():
#         print("query mismatch: %s != %s" % (query, h.get_query()))
#
#     # assert fragment == h.get_hash()
#     if not fragment == h.get_hash():
#         print("fragment mismatch: %s != %s" % (fragment, h.get_hash()))
#
#     # assert urlString == h.get_url_string()
#     if not urlString == h.get_url_string():
#         print("urlString mismatch: %s != %s" % (urlString, h.get_url_string()))
#
#     # assert pathQuery == h.get_path_query()
#     if not pathQuery == h.get_path_query():
#         print("pathQuery mismatch: %s != %s" % (pathQuery, h.get_path_query()))
#
#     print("Correct case!")
#
#
# parse_test()
