import re
from HandyURL import HandyURL

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
        self.STRAY_SPACING = "[\n\r\t\\p{Zl}\\p{Zp}\u0085]+"
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

    def url_to_scheme(self, url: str) -> str:
        for scheme in self.ALL_SCHEMES:
            if url.startswith(scheme):
                return scheme
        return None

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
        if url_string.startswith(self.DNS_SCHEME) or url_string.startswith(self.FILEDESC_SCHEME) or url_string.startswith(self.WARCINFO_SCHEME):
            h = HandyURL()
            h.set_opaque(url_string)
            return h
        url_string = self.add_default_scheme_if_needed(url_string)
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

        at_index = uri_authority.index(self.COMMERCIAL_AT)
        port_colon_index = uri_authority.index(self.COLON, 0 if at_index < 0 else at_index)

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
            pass_colon_index = user_info.index(self.COLON)
            if pass_colon_index == -1:  # no password
                user_name = user_info
            else:
                user_name = user_info[:pass_colon_index]
                user_pass = user_info[pass_colon_index + 1:]
        return HandyURL(uri_scheme, user_name, user_pass, hostname, port, uri_path, uri_query, uri_fragment)
