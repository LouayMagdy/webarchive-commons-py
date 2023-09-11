class CRC32:
    _CRC32_POLYNOMIAL = 0xEDB88320
    _CRC32_TABLE = []

    def __init__(self):
        self._crc = 0xFFFFFFFF
        if not CRC32._CRC32_TABLE:
            CRC32._CRC32_TABLE = CRC32.generate_crc_table()

    def update(self, byte_arr: bytearray = None, offset: int = 0, length: int = None, num: int = None):
        if num is not None:
            self._crc = (self._crc >> 8) ^ CRC32._CRC32_TABLE[(self._crc ^ num) & 0xFF]
        elif byte_arr is not None:
            if length is None:
                length = len(byte_arr)
            for b in byte_arr[offset: offset + length]:
                self._crc = (self._crc >> 8) ^ CRC32._CRC32_TABLE[(self._crc ^ b) & 0xFF]

    def get_value(self):
        return self._crc ^ 0xFFFFFFFF

    @staticmethod
    def generate_crc_table():
        table = [0] * 256
        for i in range(256):
            table[i] = i
            for _ in range(8):
                lsb = table[i] & 1 == 1
                table[i] >>= 1
                if lsb:
                    table[i] ^= CRC32._CRC32_POLYNOMIAL
        return table

#
# crc = CRC32()
# crc.update(num=1598764)
# crc.update(byte_arr=bytearray("Hello, World!", 'utf-8'))
# crc.update(num=2 ** 31 - 1)
# print(hex(crc.get_value()))
# 0xb267754d
