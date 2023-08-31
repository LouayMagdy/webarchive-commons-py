import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from Resource import *


class AbstractResource(Resource):
    def __init__(self, metadata, resource_container):
        self._metadata = metadata
        self._resource_container = resource_container

    def get_container(self):
        return self._resource_container

    def get_input_stream(self):
        pass

    def get_meta_data(self):
        return self._metadata

    def dump(self, out, resource):
        m = resource.get_meta_data()
        out.write("Headers Before\n")
        out.write(str(m) + "\n")

        out.write("Resource Follows:\n===================\n")
        out.write(resource.get_input_stream().read().decode())

        out.write("[\n]Headers After\n")
        out.write(str(m) + "\n")

    def dump_short(self, out, resource):
        m = resource.get_meta_data()
        byte_count = 0
        chunk_size = 4096
        while True:
            chunk = resource.get_input_stream().read(chunk_size)
            if not chunk:
                break
            byte_count += len(chunk)
        out.write(f"Resource Was: {byte_count} Long\n")

        out.write("[\n]Headers After\n")
        out.write(str(m) + "\n")


