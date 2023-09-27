from abc import abstractmethod, ABC
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from my_resource.ResourceContainer import ResourceContainer
from my_resource.MetaData import MetaData


class Resource(ABC):
    @abstractmethod
    def get_container(self) -> ResourceContainer:
        pass

    @abstractmethod
    def get_input_stream(self):
        pass

    @abstractmethod
    def get_meta_data(self) -> MetaData:
        pass
