from abc import abstractmethod, ABC


class ResourceContainer(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_compressed(self) -> bool:
        pass
