import tldextract


class HandyURL:
    def __init__(self, scheme: str = None, auth_user: str = None,
                 auth_pass: str = None, host: str = None, port: int = None,
                 path: str = None, query: str = None, hashing: str = None):
        self.DEFAULT_PORT = -1
        self.scheme = scheme
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.host = host
        self.port = port
        self.path = path
        self.query = query
        self.hashing = hashing  # hash in java is renamed to hashing here because name is reserved
        self.opaque = None
        self.cached_pub_suffix = None
        self.cached_pub_prefix = None

    def get_SURT_string(self, include_scheme):
        return self.get_url_string(True, include_scheme, False)

    # Helping function
    def _host_to_SURT(self, host: str) -> str:
        parts = host.split(".", -1)
        if len(parts) == 1:
            return host
        sb = ""
        for i in range(len(parts) - 1, 0, -1):
            sb += parts[i] + ","
        sb += parts[0]
        return sb

    # Helping function
    def _host_to_public_suffix(self, host: str):
        extracted = tldextract.extract(host)
        if extracted.suffix:
            return extracted.registered_domain
        return host

    def get_url_string(self, surt=False, include_scheme=True, public_suffix=False):  # Not tested
        if self.opaque is not None:
            return self.opaque
        sb = []
        if include_scheme:
            sb.append(self.scheme + "://")
            if surt:
                sb.append("(")
        if self.auth_user is not None:
            sb.append(self.auth_user)
            if self.auth_pass is not None:
                sb.append(":" + self.auth_pass)
            sb.append('@')
        host_src = self.host
        if public_suffix:
            host_src = self.get_public_suffix()
        if surt:
            host_src = self._host_to_SURT(host_src)
        sb.append(host_src)
        if self.port != self.DEFAULT_PORT:
            sb.append(":" + str(self.port))
        if surt:
            sb.append(")")
        hash_path = self.path is not None and len(self.path) > 0
        if hash_path:
            sb.append(self.path)
        else:
            if self.query is not None or self.hashing is not None:
                sb.append("/")
        if self.query is not None:
            sb.append("?" + self.query)
        if self.hashing is not None:
            sb.append("#" + self.hashing)
        return "".join(sb)

    def get_path_query(self):  # not tested
        sb = ""
        has_path = (self.path is not None) and (len(self.path) > 0)
        if has_path:
            sb += self.path
        else:
            if (self.query is not None) or (self.hashing is not None):
                sb += "/"
        if self.query is not None:
            sb += '?' + self.query
        return sb

    def get_public_suffix(self): # not tested
        if self.cached_pub_suffix is not None:
            return self.cached_pub_suffix
        if self.host is None:
            return None
        self.cached_pub_suffix = self._host_to_public_suffix(self.host) # needs testing
        return self.cached_pub_suffix

    def get_public_prefix(self): # not tested
        if self.cached_pub_prefix is not None:
            return self.cached_pub_prefix
        if self.host is None:
            return None
        pub_s = self.get_public_suffix()
        if pub_s is None:
            return None
        host_len = len(self.host)
        host_len -= len(pub_s)
        if host_len > 1:
            self.cached_pub_prefix = self.host[0:(len(self.host) - len(pub_s)) - 1]
        else:
            self.cached_pub_prefix = ""
        return self.cached_pub_prefix

    def get_scheme(self) -> str:
        return self.scheme

    def set_scheme(self, scheme: str):
        self.scheme = scheme

    def get_auth_user(self) -> str:
        return self.auth_user

    def set_auth_user(self, auth_user: str):
        self.auth_user = auth_user

    def get_auth_pass(self) -> str:
        return self.auth_pass

    def set_auth_pass(self, auth_pass: str):
        self.auth_pass = auth_pass

    def get_host(self):
        return self.host

    def set_host(self, host: str):
        self.host = host
        self.cached_pub_prefix = None
        self.cached_pub_suffix = None

    def get_port(self) -> int:
        return self.port

    def set_port(self, port: int):
        self.port = port

    def get_path(self) -> str:
        return self.path

    def set_path(self, path: str):
        self.path = path

    def get_query(self):
        return self.query

    def set_query(self, query: str):
        self.query = query

    def get_hash(self) -> str:
        return self.hashing

    def set_hash(self, hashing: str):
        self.hashing = hashing

    def get_opaque(self) -> str:
        return self.opaque

    def set_opaque(self, opaque: str):
        self.opaque = opaque

    def to_debug_string(self):
        return "Scheme({}) UserName({}) UserPass({}) Host({}) Port({}) Path({}) Query({}) Frag({})".format(
            self.scheme, self.auth_user, self.auth_pass, self.host,
            self.port, self.path, self.query, self.hashing
        )


    ############# Function not implemented, as it is unused by any other part, and it requires much time! #############
    # public URL toURL() throws MalformedURLException {
    #     return new URL(getURLString());
    # }


################# Testing ################

# handyURL = HandyURL("http", "user", "pass", "example.com", -1, "/path", "query", "hash")
# urlString = handyURL.get_url_string()
# pathQuery = handyURL.get_path_query()
# print(f"urlString = {urlString}\npathQuery = {pathQuery}\n======")
#
# handyURL2 = HandyURL()
# handyURL2.set_host("example.co.uk")
# publicSuffix = handyURL2.get_public_suffix()
# print(f"publicSuffix = {publicSuffix}\n======")
#
# handyURL3 = HandyURL()
# handyURL3.set_host("www.example.com")
# publicPrefix = handyURL3.get_public_prefix()
# print(f"publicPrefix = {publicPrefix}\n======")
#
# # ************************************
#
# handyURL = HandyURL("https", "user", "pass", "example.com", 8080, "/path", "query", "hash")
# urlString = handyURL.get_url_string(True, True, True)
# print(f"urlString = {urlString}\n======")
# # Assert that urlString is equal to "https://(com,example,)/path?query#hash"
#
# handyURL = HandyURL("http", "user", "pass", "example.com", -1, None, "query", None)
# pathQuery = handyURL.get_path_query()
# print(f"pathQuery = {pathQuery}\n======")
# # Assert that pathQuery is equal to "/?query"
#
# handyURL = HandyURL()
# publicSuffix = handyURL.get_public_suffix()
# print(f"publicSuffix = {publicSuffix}\n======")
# # Assert that publicSuffix is None
#
# handyURL = HandyURL()
# publicPrefix = handyURL.get_public_prefix()
# print(f"publicPrefix = {publicPrefix}\n======")
# # Assert that publicPrefix is None
#
# handyURL = HandyURL("ftp", "user", "pass", "example.com", 21, "/path", None, None)
# urlString = handyURL.get_url_string(False, False, False)
# print(f"urlString = {urlString}\n======")
# # Assert that urlString is equal to "//user:pass@example.com:21/path"
#
# handyURL = HandyURL("http", "user", None, "example.com", -1, None, None, None)
# pathQuery = handyURL.get_path_query()
# print(f"pathQuery = {pathQuery}\n======")
# # Assert that pathQuery is an empty string
#
# handyURL = HandyURL()
# handyURL.set_host("192.168.0.1")
# publicSuffix = handyURL.get_public_suffix()
# print(f"publicSuffix = {publicSuffix}\n======")
# # Assert that publicSuffix is None
#
# handyURL = HandyURL()
# handyURL.set_host("subdomain.example.com")
# publicPrefix = handyURL.get_public_prefix()
# print(f"publicPrefix = {publicPrefix}\n======")
# # Assert that publicPrefix is None
#
# # handyURL = HandyURL("https", None, None, "example.com", -1, "/path", None, None)
# # url = handyURL.toURL()
# # print(f"url = {url}\n======")
# # # Assert that url is a valid URL object representing "https://example.com/path"
#
# handyURL = HandyURL("http", None, None, "example.com", -1, None, None, None)
# scheme = handyURL.get_scheme()
# print(f"scheme = {scheme}\n======")
# # Assert that scheme is equal to "http"
#
# handyURL = HandyURL("ftp", "user", "pass", "example.com", 21, "/path", "query", "hash")
# debugString = handyURL.to_debug_string()
# print(f"debugString = {debugString}\n======")
# # Assert that debugString is equal to "Scheme(ftp) UserName(user) UserPass(pass) Host(example.com) port(21) Path(/path) Query(query) Frag(hash)"





