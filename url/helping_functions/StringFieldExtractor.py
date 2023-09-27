class StringFieldExtractor:
    def __init__(self, delim, field):
        self.delim = delim
        self.field = field

    def split(self, s):
        keyEnd = 0
        for i in range(self.field):
            dIdx = s.find(self.delim, keyEnd)
            if dIdx == -1:
                return s, None
            keyEnd = dIdx + 1
        return s[:keyEnd - 1], s[keyEnd:]

    # def extract(self, text):
    #     if text is None:
    #         return None
    #     start = 0
    #     for i in range(self.field):
    #         if start > len(text):
    #             return None
    #         newStart = text.find(self.delim, start)
    #         if newStart == -1:
    #             return None
    #         start = newStart + 1
    #     if start == len(text):
    #         return ""
    #     end = text.find(self.delim, start)
    #     if end == -1:
    #         return text[start:]
    #     else:
    #         return text[start:end]
