import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from my_resource.ResourceProducer import ResourceProducer
from my_resource.ResourceContainer import ResourceContainer
from my_resource.MetaData import MetaData
from my_resource.generic.GenericStreamResource import GenericStreamResource


class GenericResourceProducer(ResourceProducer, ResourceContainer):
    _unlimited = -1

    def __init__(self, stream, name, end_offset=_unlimited):
        self.stream = stream
        self.name = name
        self.end_offset = end_offset

    def get_next(self):
        if (self.stream.tell() == os.fstat(self.stream.fileno()).st_size) or (
                self.end_offset != self._unlimited and self.stream.tell() > self.end_offset):
            return None
        return GenericStreamResource(MetaData(), self, self.stream)
    def _get_name(self):
        return self.name

    def is_compressed(self):
        return False

    def close(self):
        self.stream.close()

    def get_context(self):
        return f"Context{self.name}{self.stream.tell()}"
