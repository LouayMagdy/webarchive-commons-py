import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from my_resource.MetaData import MetaData


class ResourceParseException(Exception):
    def __init__(self, e, metaData: MetaData = None):
        super().__init__(str(e))
        self.metaData = metaData
