import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from formats.gzip.GZIPMemberSeries import GZIPMemberSeries
from formats.gzip.GZIPSeriesMember import GZIPSeriesMember
from my_resource.MetaData import MetaData
from my_resource.Resource import Resource
from my_resource.ResourceContainer import ResourceContainer
from my_resource.ResourceProducer import ResourceProducer
from my_resource.ResourceParseException import ResourceParseException


class GZIPResourceContainer(ResourceProducer, ResourceContainer):
    _UNLIMITED = -1

    def __init__(self, series: GZIPMemberSeries, end_offset: int = _UNLIMITED):
        self._series = series
        self._end_offset = end_offset

    def get_name(self) -> str:
        return self._series.get_stream_context()

    def is_compressed(self) -> bool:
        return True

    def get_next(self) -> Resource | None:
        if self._series.got_eof() or (self._end_offset != self._UNLIMITED and self._series.get_offset() > self._end_offset):
            return None
        member = self._series.get_next_member()
        if member is None:
            return None
        top = MetaData()
        # implement Gzip Resource




