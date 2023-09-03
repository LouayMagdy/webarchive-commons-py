import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from my_resource.generic.GenericResourceProducer import GenericResourceProducer

class EnvelopedResourceFile:
    def __init__(self, resource_factory):
        self.factory = resource_factory
        self.strict = True
        self.start_offset = 0

    def get_producer(self, stream, name):
        producer = GenericResourceProducer(stream, name)


