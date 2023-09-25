from abc import ABC, abstractmethod


class HttpResponseMessageObserver(ABC):
    @abstractmethod
    def message_parsed(self, version: int, code: int, reason: str, bytes: int):
        pass

    @abstractmethod
    def message_corrupt(self):
        pass
