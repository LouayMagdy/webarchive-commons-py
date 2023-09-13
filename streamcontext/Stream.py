from abc import ABC, abstractmethod
from io import IOBase


class Stream(ABC, IOBase):
    """
        Alternate simplified interface for accessing data from an underlying source of bytes
    """

    @abstractmethod
    def get_offset(self) -> int:
        pass

    @abstractmethod
    def set_offset(self, offset: int) -> int:
        pass

    @abstractmethod
    def read(self, byte_arr: bytearray, offset: int, length: int) -> int:
        pass

    @abstractmethod
    def is_at_eof(self) -> bool:
        pass
