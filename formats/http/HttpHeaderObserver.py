from abc import ABC, abstractmethod


class HttpHeaderObserver(ABC):
    @abstractmethod
    def header_parsed(self, name: bytearray, name_start: int, name_length: int,
                           value: bytearray, value_start: int, value_length: int):
        pass

    @abstractmethod
    def headers_complete(self, total_bytes: int):
        pass

    @abstractmethod
    def headers_corrupt(self):
        pass
