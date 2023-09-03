import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from my_resource.ResourceProducer import ResourceProducer
from my_resource.ResourceFactory import ResourceFactory


class TransformingResourceProducer(ResourceProducer):

    def __init__(self, resource_producer: ResourceProducer, resource_factory: ResourceFactory):
        self._resource_producer = resource_producer
        self._resource_factory = resource_factory

    def get_next(self):
        inner_resource = self._resource_producer.get_next()
        if inner_resource is None:
            return None
        return self._resource_factory.get_resource(
            inner_resource.get_input_stream(), inner_resource.get_meta_data(), inner_resource.get_container())

    def close(self):
        self._resource_producer.close()

    def get_context(self):
        return self._resource_producer.get_context()
