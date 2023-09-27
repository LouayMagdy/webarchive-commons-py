import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from my_resource.Resource import Resource
from my_resource.MetaData import MetaData
from my_resource.ResourceContainer import ResourceContainer


class AbstractResource(Resource):
    def __init__(self, metadata: MetaData, resource_container: ResourceContainer):
        self._metadata = metadata
        self._resource_container = resource_container

    def get_container(self) -> ResourceContainer:
        return self._resource_container

    def get_input_stream(self):
        pass

    def get_meta_data(self) -> MetaData:
        return self._metadata

    def dump(self, print_stream_out, resource: Resource):
        m = resource.get_meta_data()
        print_stream_out.write("Headers Before\n")
        print_stream_out.write(str(m) + "\n")

        print_stream_out.write("Resource Follows:\n===================\n")
        print_stream_out.write(resource.get_input_stream().read().decode())

        print_stream_out.write("[\n]Headers After\n")
        print_stream_out.write(str(m) + "\n")

    def dump_short(self, print_stream_out, resource: Resource):
        m = resource.get_meta_data()
        byte_count = 0
        chunk_size = 4096
        while True:
            chunk = resource.get_input_stream().read(chunk_size)
            if not chunk:
                break
            byte_count += len(chunk)
        print_stream_out.write(f"Resource Was: {byte_count} Long\n")

        print_stream_out.write("[\n]Headers After\n")
        print_stream_out.write(str(m) + "\n")
