import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from my_resource.ResourceProducer import ResourceProducer
from my_resource.producer.EnvelopedResourceFile import EnvelopedResourceFile


class ProducerUtils:
    STRICT_GZ = False

    @staticmethod
    def get_producer(self, path: str, offset: int = 0):
        producer = None
        ef, af, wf = EnvelopedResourceFile(), ...
        ef.set_strict(self.STRICT_GZ)





