from ..ResourceFactory import ResourceFactory
from ..ResourceContainer import ResourceContainer


class GenericResourceProducer(ResourceFactory, ResourceContainer):
    _unlimited = -1

    def __init__(self, stream, name, end_offset=_unlimited):
        self.stream = stream
        self.name = name
        self.end_offset = end_offset

    def get_resource(self, input_stream, parent_meta_data, container):
        pass #here

    def get_name(self):
        return self.name

    def is_compressed(self):
        return False
