from abc import ABC, abstractmethod


class EOFObserver(ABC):
    @abstractmethod
    def notify_eof(self):
        pass
