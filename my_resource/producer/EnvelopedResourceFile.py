
class EnvelopedResourceFile:
    def __init__(self, resource_factory):
        self.factory = resource_factory
        self.strict = True
        self.start_offset = 0

    def get_producer(self, stream, name):
