import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from formats.gzip.GZIPConstants import GZIPConstants
from formats.gzip.GZIPSeriesMember import GZIPSeriesMember
from my_resource.AbstractResource import AbstractResource
from my_resource.MetaData import MetaData
from my_resource.ResourceConstants import ResourceConstants
from my_resource.ResourceContainer import ResourceContainer
from my_resource.gzip.GZIPMetaData import GZIPMetaData
from utils.io.EOFObserver import EOFObserver
from utils.io.EOFNotifyingInputStream import EOFNotifyingInputStream


class GZIPResource(AbstractResource, EOFObserver):

    def __init__(self, metadata: MetaData, resource_container: ResourceContainer, gzip_member: GZIPSeriesMember):
        super().__init__(metadata, resource_container)
        self._gzip_series_member = gzip_member
        self._eof_stream = EOFNotifyingInputStream(gzip_member, self)

        container_meta_data = MetaData(metadata, ResourceConstants.get("CONTAINER"))
        container_meta_data.put(ResourceConstants.get("CONTAINER_FILENAME"), gzip_member.get_record_file_context())
        container_meta_data.put(ResourceConstants.get("CONTAINER_COMPRESSED"), True)
        container_meta_data.put(ResourceConstants.get("CONTAINER_OFFSET"), gzip_member.get_record_start_offset())
        self._gz_meta_data = GZIPMetaData(container_meta_data)

    def close(self):
        self._gzip_series_member.close()

    def get_input_stream(self):
        return self._eof_stream

    def notify_eof(self):
        self._gz_meta_data.set_data(self._gzip_series_member)
