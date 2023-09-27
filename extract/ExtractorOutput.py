from abc import ABC, abstractmethod
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from my_resource.Resource import Resource


class ExtractorOutput(ABC):
    @abstractmethod
    def output(self, resource: Resource):
        pass
