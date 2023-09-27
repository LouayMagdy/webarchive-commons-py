import re


class RewriteRule:
    def __init__(self):
        self.starts_with = None
        self.regex = None
        self.replace = None
        self.regex_pattern = None

    def get_starts_with(self):
        return self.starts_with

    def set_starts_with(self, starts_with):
        self.starts_with = starts_with

    def get_regex(self):
        return self.regex

    def set_regex(self, regex):
        self.regex_pattern = re.compile(regex)
        self.regex = regex

    def get_replace(self):
        return self.replace

    def set_replace(self, replace):
        self.replace = replace

    def rewrite(self, sb: str): # sb is a string
        urlkey = str(sb)
        if self.starts_with is not None and not urlkey.startswith(self.starts_with):
            return False
        if self.regex_pattern is None or self.replace is None:
            return False
        match = self.regex_pattern.match(urlkey)
        if match:
            re.sub(self.regex_pattern, self.replace, urlkey)
            return True
        return False

#
# test = RewriteRule()
# test.set_starts_with("http://")
# test.set_regex("^http://example\\.com/(\\d+)$")
# test.set_replace("http://www.example.com/$1")
# print(test.rewrite("http://example.com/123"))
#
# test = RewriteRule()
# test.set_starts_with("https://")
# test.set_regex("^http://example\\.com/(\\d+)$")
# test.set_replace("http://www.example.com/$1")
# print(test.rewrite("http://example.com/123"))
#
# # test = RewriteRule()
# # test.set_starts_with("http://")
# # test.set_regex(None)
# # test.set_replace(None)
# # print(test.rewrite("http://example.com/123"))


