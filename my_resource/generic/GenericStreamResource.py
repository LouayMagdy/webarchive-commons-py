import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from my_resource.MetaData import MetaData
from my_resource.ResourceConstants import ResourceConstants
from my_resource.AbstractResource import AbstractResource
from streamcontext.StreamWrappedInputStream import StreamWrappedInputStream


class GenericStreamResource(AbstractResource):
    def __init__(self, metadata, resource_container, stream):
        super().__init__(metadata, resource_container)
        self._stream = stream
        container_meta_data = MetaData(metadata, ResourceConstants.get("CONTAINER"))
        container_meta_data.put(ResourceConstants.get("CONTAINER_FILENAME"), resource_container.getName());
        container_meta_data.put(ResourceConstants.get("CONTAINER_COMPRESSED"), resource_container.isCompressed());
        container_meta_data.put(ResourceConstants.get("CONTAINER_OFFSET"), stream.getOffset());

    def get_input_stream(self):
        return StreamWrappedInputStream(self._stream)


### REMEMBER THAT: stream is an opened file !!!!!
