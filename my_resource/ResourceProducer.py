from abc import abstractmethod, ABC
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from my_resource.Resource import Resource


class ResourceProducer(ABC):
    @abstractmethod
    def get_next(self) -> Resource | None:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_context(self) -> str:
        pass
