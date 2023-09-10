from abc import abstractmethod


class PushBackOneByteInputStream:
    @abstractmethod
    def push_back(self):
        pass

    @abstractmethod
    def read(self) -> int:
        pass
