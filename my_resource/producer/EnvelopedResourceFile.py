import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

# some package from Hadoop --------------------------
from formats.gzip.GZIPMemberSeries import GZIPMemberSeries
from my_resource.ResourceProducer import ResourceProducer
from my_resource.ResourceFactory import ResourceFactory
from my_resource.TransformingResourceProducer import TransformingResourceProducer
from my_resource.generic.GenericResourceProducer import GenericResourceProducer
from streamcontext.Stream import Stream


class EnvelopedResourceFile:
    def __init__(self, resource_factory: ResourceFactory):
        self._resource_factory = resource_factory
        self.strict = True
        self.start_offset = 0

    def get_producer(self, stream, name) -> ResourceProducer:
        producer = GenericResourceProducer(stream, name)
        return TransformingResourceProducer(producer, self._resource_factory)

    def get_GZ_producer(self, stream, name) -> ResourceProducer:

