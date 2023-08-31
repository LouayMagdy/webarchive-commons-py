from abc import abstractmethod


class ResourceFactory:
    @abstractmethod
    def get_resource(self, input_stream, parent_meta_data, container):
        """
        Attempts to create a Resource from the InputStream
        may raise ResourceParseException, IOException
        :param input_stream
        :param parent_meta_data
        :param container
        """
        pass
