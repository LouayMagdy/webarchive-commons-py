from abc import abstractmethod

class ResourceProducer:
    @abstractmethod
    def get_next(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_context(self):
        pass