import logging


def add_logger(cls):
    cls.logger = logging.getLogger(cls.__name__)
    return cls


@add_logger
class URI:
    x = 5


print(URI.logger)
