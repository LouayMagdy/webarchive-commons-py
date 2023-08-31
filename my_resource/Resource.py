from abc import abstractmethod


class Resource:
    @abstractmethod
    def get_container(self):
        pass

    @abstractmethod
    def get_input_stream(self):
        pass

    @abstractmethod
    def get_meta_data(self):
        pass
