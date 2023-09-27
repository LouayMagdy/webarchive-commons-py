from abc import abstractmethod, ABC


class PushBackOneByteInputStream(ABC):
    @abstractmethod
    def push_back(self):
        pass

    @abstractmethod
    def read(self) -> int:
        pass
