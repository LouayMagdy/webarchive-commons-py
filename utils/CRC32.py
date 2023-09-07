class CRC32:
    CRC32_POLYNOMIAL = 0xEDB88320
    CRC32_TABLE = []

    def __init__(self):
        self.crc = 0xFFFFFFFF
        if not CRC32.CRC32_TABLE:
            CRC32.CRC32_TABLE = CRC32.generate_crc_table()

    def update(self, byte_arr: bytearray = None, num: int = None):
        if num is not None:
            self.crc = (self.crc >> 8) ^ CRC32.CRC32_TABLE[(self.crc ^ num) & 0xFF]
        elif byte_arr is not None:
            for b in byte_arr:
                self.crc = (self.crc >> 8) ^ CRC32.CRC32_TABLE[(self.crc ^ b) & 0xFF]

    def get_value(self):
        return self.crc ^ 0xFFFFFFFF

    @staticmethod
    def generate_crc_table():
        table = [0] * 256
        for i in range(256):
            table[i] = i
            for _ in range(8):
                lsb = table[i] & 1 == 1
                table[i] >>= 1
                if lsb:
                    table[i] ^= CRC32.CRC32_POLYNOMIAL
        return table


crc = CRC32()
crc.update(num=1598764)
crc.update(byte_arr=bytearray("Hello, World!", 'utf-8'))
crc.update(num=2 ** 31 - 1)
print(hex(crc.get_value()))
# 0xb267754d
