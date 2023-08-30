from ..AbstractResource import AbstractResource
from ..ResourceConstants import ResourceConstants
from ..MetaData import MetaData
class GenericStreamResource(AbstractResource):
    def __init__(self, metadata, resource_container, stream):
        super().__init__(metadata, resource_container)
        self._stream = stream
        container_meta_data = MetaData(metadata, ResourceConstants.get("CONTAINER"))
        container_meta_data.put(ResourceConstants.get("CONTAINER_FILENAME"), resource_container.getName());
        container_meta_data.put(ResourceConstants.get("CONTAINER_COMPRESSED"), resource_container.isCompressed());
        container_meta_data.put(ResourceConstants.get("CONTAINER_OFFSET"), stream.getOffset());

    def get_input_stream(self):
