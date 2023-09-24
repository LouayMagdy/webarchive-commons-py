import sys
import os
from urllib.parse import urlparse

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from formats.gzip.GZIPMemberSeries import GZIPMemberSeries
from my_resource.ResourceProducer import ResourceProducer
from my_resource.ResourceFactory import ResourceFactory
from my_resource.TransformingResourceProducer import TransformingResourceProducer
from my_resource.generic.GenericResourceProducer import GenericResourceProducer
from my_resource.gzip.GZIPResourceContainer import GZIPResourceContainer
from streamcontext.Stream import Stream
from streamcontext.RandomAccessFileStream import RandomAccessFileStream
from streamcontext.HTTP11Stream import HTTP11Stream
from streamcontext.HDFSStream import HDFSStream


class EnvelopedResourceFile:
    def __init__(self, resource_factory: ResourceFactory):
        self._resource_factory = resource_factory
        self._strict = True
        self._start_offset = 0

    def get_producer(self, stream, name: str, gz: bool = False) -> ResourceProducer:
        if gz:
            producer = GenericResourceProducer(stream, name)
            return TransformingResourceProducer(producer, self._resource_factory)
        else:
            series = GZIPMemberSeries(stream, name, self._start_offset, self._strict)
            producer = GZIPResourceContainer(series)
            return producer if not self._resource_factory else TransformingResourceProducer(producer,
                                                                                        self._resource_factory)
    def get_resource_producer(self, is_gz: bool = False,file = None, hdfs_file_url_path: str = None, url: str= None,
                              offset: int = 0):
        if file:
            stream = RandomAccessFileStream(file)
            if offset > 0:
                stream.set_offset(offset)
            return self.get_producer(stream, os.path.basename(file.name), is_gz)
        elif hdfs_file_path:
            parsed_url = urlparse(hdfs_file_url_path)
            stream = HDFSStream(parsed_url.scheme + parsed_url.netloc, parsed_url.path)
            if offset > 0:
                stream.set_offset(offset)
            return self.get_producer(stream, parsed_url.path.split('/')[-1], is_gz)
        elif url:
            stream = HTTP11Stream(url)
            if offset > 0:
                stream.set_offset(offset)
            name = urlparse(url).paht.split('/')[-1]
            if name == '' or len(name) == 0:
                name = 'UNKNOWN'
            return self.get_producer(stream, name, is_gz)

    def is_strict(self):
        return self._strict

    def set_strict(self, strict: bool):
        self._strict = strict

    def get_start_offset(self):
        return self._start_offset

    def set_start_offset(self, start_offset: int):
        self._start_offset = start_offset
