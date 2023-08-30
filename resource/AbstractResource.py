from Resource import Resource
import json


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

    def dump(self, file_path, resource):
        m = resource.get_meta_data()
        with open(file_path, 'a') as f:
            f.write("Headers Before\n")
            f.write(json.dumps(m))
            f.write("\nResource Follows:\n===================\n")
            f.write(resource.get_input_stream().read())
            f.write("\n[\n]Headers After\n")
            f.write(json.dumps(m))
            f.write("\n")

    def dump_short(self, file_path, resource) -> None:
        m = resource.get_meta_data()
        m_bytes = resource.get("input_stream").read()
        with open(file_path, 'a') as f:
            f.write(f"Resource Was: {len(m_bytes)} Long\n")
            f.write("[\n]Headers After\n")
            f.write(json.dumps(m))
            f.write("\n")

