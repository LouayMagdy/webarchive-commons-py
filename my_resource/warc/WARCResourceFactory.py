import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from my_resource.ResourceFactory import ResourceFactory
from my_resource.ResourceConstants import ResourceConstants


class WARCResourceFactory(ResourceFactory):
