import re
import os
import string
from collections import namedtuple
from HandyURL import HandyURL
from .CanonicalizerConstants import CanonicalizerConstants as consts
from .URLCanonicalizer import URLCanonicalizer as urlcan
from CanonicalizeRules import CanonicalizeRules

class IAURLCanonicalizer:
    def __init__(self, rules: CanonicalizeRules):
        self.rules: CanonicalizeRules = rules

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
    def _strip_query_session_id(self, query):
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
            url.set_host(self.massage_host(url.get_host()))

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
                path = self._strip_path_session_id(path)

            if self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_STRIP_EMPTY):
                url.set_path(None)
            elif self.rules.is_set(consts.PATH_SETTINGS, consts.PATH_STRIP_TRAILING_SLASH_UNLESS_EMPTY):
                if os.path.exists(path) and path.endswith('/') and len(path) > 1:
                    path = path[0:len(path)-1]
            url.set_path(path)

        query: str = url.get_query()
        if query is not None:
            # we have a query... what to do with it?
            # 1st: remove unneeded:
            if self.rules.is_set(consts.QUERY_SETTINGS, consts.QUERY_STRIP_SESSION_ID):
                query = self._strip_query_session_id(query)
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


    def massage_host(self, host: str) -> str:
        pass

    def alpha_reorder_query(self, orig: str) -> str:
        pass

