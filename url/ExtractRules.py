import re


class ExtractRule:
    def __init__(self):
        self.starts_with = None
        self.regex = None
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

    def extract(self, url):
        if self.starts_with is not None and not self.starts_with == '' and not url.startswith(self.starts_with):
            return None

        if self.regex_pattern is None:
            return None

        match = self.regex_pattern.search(url)

        if not match:
            return None

        return match


##################### TESTING ######################
# extractRule = ExtractRule()
#
# # Test Case 1: Matching url with startsWith and regex
# extractRule.set_starts_with("https://")
# extractRule.set_regex("example\\.com")
# matcher1 = extractRule.extract("https://example.com")
# print(matcher1.group())  # Expected: "example.com"
#
# # Test Case 3: Matching url with regex but no startsWith
# extractRule.set_starts_with(None)
# extractRule.set_regex("example\\.com")
# matcher3 = extractRule.extract("https://example.com")
# print(matcher3.group())  # Expected: "example.com"
#
# # Test Case 4: Non-matching url with startsWith and regex
# extractRule.set_starts_with("https://")
# extractRule.set_regex("example\\.com")
# matcher4 = extractRule.extract("http://example.com")
# if matcher4 is None:
#     print("NULL")
# else:
#     print(matcher4.group())  # Expected: "example.com"
#
# # Test Case 6: Non-matching url with regex but no startsWith
# extractRule.set_starts_with(None)
# extractRule.set_regex("example\\.com")
# matcher6 = extractRule.extract("http://example.com")
# if matcher6 is None:
#     print("NULL")
# else:
#     print(matcher6.group())  # Expected: "example.com"
#
# # Test Case 7: Matching url with empty startsWith and regex
# extractRule.set_starts_with("")
# extractRule.set_regex("example\\.com")
# matcher7 = extractRule.extract("http://example.com")
# if matcher7 is None:
#     print("NULL")
# else:
#     print(matcher7.group())  # Expected: "example.com"
#
#
# # Test Case 8: Non-matching url with empty startsWith and regex
# extractRule.set_starts_with("")
# extractRule.set_regex("example\\.com")
# matcher8 = extractRule.extract("https://google.com")
# if matcher8 is None:
#     print("NULL")
# else:
#     print(matcher8.group())  # Expected: "example.com"
#
# # Test Case 9: Non-matching url with empty startsWith and empty regex
# extractRule.set_starts_with("")
# extractRule.set_regex("")
# matcher9 = extractRule.extract("http://example.com")
# if matcher9 is None:
#     print("NULL")
# else:
#     print(matcher9.group())  # Expected: "example.com"
#
# # Test Case 10: Matching url with null startsWith and regex
# extractRule.set_starts_with(None)
# extractRule.set_regex("example\\.com")
# matcher10 = extractRule.extract("http://example.com")
# if matcher10 is None:
#     print("NULL")
# else:
#     print(matcher10.group())  # Expected: "example.com"
