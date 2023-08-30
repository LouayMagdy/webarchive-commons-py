import logging


class MetaData(dict):
    _logger = logging.getLogger(__name__)

    def __init__(self, parent_meta_data=None, name=None):
        super().__init__()
        if parent_meta_data is None:
            self._topMetaData = self
        else:
            self._topMetaData = parent_meta_data.get_top_meta_data()
            if name is not None:
                parent_meta_data.put(name, self)

    def get(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            self._logger.warning(e)
            return None

    def put(self, key, value):
        try:
            super().__setitem__(key, value)
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def get_top_meta_data(self):
        if self._topMetaData is None:
            return self
        return self._topMetaData

    def set_top_meta_data(self, top_meta_data):
        self._topMetaData = top_meta_data

    def create_child(self, name):
        return MetaData(self, name)

    def append_child(self, key, child):
        try:
            jarray = [self.get(key)]
            if jarray[0] is None:
                jarray = []
            self.put(key, jarray)
            jarray.append(child)
            return self
        except KeyError as e:
            self._logger.warning(e)
            return None

    def append_obj(self, key, *args):
        n = {}
        print(key, args, len(args))
        if len(args) % 2 == 1:
            raise ValueError("Odd number of arguments")
        try:
            for i in range(0, len(args), 2):
                n[args[i]] = args[i + 1]
            self.append_child(key, n)
        except KeyError as e:
            self._logger.warning(e)


# metadata = MetaData()
# metadata.put("first", 1)
# metadata.put("second", "ok")
# metadata.put("third", True)
# print(metadata.get("first"), metadata.get("second"), metadata.get("third"))
# child1 = metadata.create_child("c1")
# child2 = metadata.create_child("c2")
# metadata.append_child("c1", child2)
# metadata.append_child("c3", child2)
# print(metadata.get("c1"), metadata.get("c3"))
# metadata.append_obj("key", "a", 1, "b", 2, "c", False)
# print(metadata.get("key"))
