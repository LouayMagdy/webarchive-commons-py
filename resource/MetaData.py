import logging


class MetaData(dict):
    _logger = logging.getLogger(__name__)
    _topMetaData = None

    def __init__(self, parent_meta_data=None, name=None):
        super().__init__()
        if parent_meta_data is None:
            self._topMetaData = self
        else:
            self._topMetaData = parent_meta_data.get_top_meta_data()
        if name is not None:
            parent_meta_data.putChild(name, self)

    def get(self, key):
        try:
            return super().get(key)
        except KeyError as e:
            self._logger.warning(e)
            return None

    def get_boolean(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            self._logger.warning(e)
            return False

    def get_int(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            self._logger.warning(e)
            return -1

    def get_long(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            self._logger.warning(e)
            return -1

    def get_string(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            self._logger.warning(e)
            return None

    def create_child(self, name):
        return MetaData(self, name)

    def get_top_meta_data(self):
        if self._topMetaData is None:
            return self
        return self._topMetaData

    def set_top_meta_data(self, top_meta_data):
        self._topMetaData = top_meta_data

    def put_string(self, key, value):
        try:
            super().__setitem__(key, value)
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def put_long(self, key, value):
        try:
            super().__setitem__(key, str(value))
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def put_boolean(self, key, value):
        try:
            super().__setitem__(key, value)
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def put_child(self, key, child):
        try:
            super().__setitem__(key, child)
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def append_child(self, key, child):
        try:
            jarray = self.get(key)
            if jarray is None:
                jarray = []
                self[key] = jarray
            jarray.append(child)
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def append_obj(self, key, *args):
        n = {}
        if len(args) % 2 == 1:
            raise ValueError("Odd number of arguments")
        try:
            for i in range(0, len(args), 2):
                n[args[i]] = args[i + 1]
            self.append_child(key, n)
        except KeyError as e:
            self._logger.warning(e)

# class MetaDataEncoder:
