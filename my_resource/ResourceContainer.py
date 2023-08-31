from abc import abstractmethod


class ResourceContainer:
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def is_compressed(self):
        pass
