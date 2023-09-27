import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from my_resource.producer.EnvelopedResourceFile import EnvelopedResourceFile

class WARCFile(EnvelopedResourceFile):
