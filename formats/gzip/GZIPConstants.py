GZIPConstants = {
    "GZIP_STATIC_HEADER_SIZE": 10,
    "GZIP_STATIC_FOOTER_SIZE": 8,
    "NO_BYTES_IN_STREAM": "No bytes in stream",
    "GZIP_MAGIC_ONE_IDX": 0,
    "GZIP_MAGIC_ONE": 0x1f,
    "GZIP_MAGIC_TWO_IDX": 1,
    "GZIP_MAGIC_TWO": 0x8b,
    "GZIP_COMPRESSION_METHOD_IDX": 2,
    "GZIP_COMPRESSION_METHOD_DEFLATE": 0x08,
    "GZIP_FLAG_IDX": 3,
    "GZIP_FLAG_FTEXT": 0x01,
    "GZIP_FLAG_FHCRC": 0x02,
    "GZIP_FLAG_FEXTRA": 0x04,
    "GZIP_FLAG_FNAME": 0x08,
    "GZIP_FLAG_FCOMMENT": 0x10,
    "GZIP_FLAG_VALID_BITS": 0x01 | 0x02 | 0x04 | 0x08 | 0x10,
    "GZIP_MTIME_IDX": 4,
    "GZIP_MTIME_LENGTH": 4,
    "GZIP_XFL_IDX": 8,
    "GZIP_OS_IDX": 9,
    "GZIP_OS_UNIX": 0x03,
    "GZIP_FEXTRA_NAME_BYTES": 2,
    "GZIP_FEXTRA_LENGTH_BYTES": 2,
    "GZIP_FEXTRA_VALUE_MAX_LENGTH": 65536,
    "GZIP_FEXTRA_NAME_IDX": 0,
    "GZIP_FEXTRA_LENGTH_IDX": 2,
    "GZIP_FEXTRA_VALUE_IDX": 4,
    "LX_RECORD": {'L', 'X'},
    "LX_RECORD_VALUE": {0, 0, 0, 0},
    "SL_RECORD": {'S', 'L'},
    "BYTES_IN_SHORT": 2,
    "BYTES_IN_INT": 4,
    "GZIP_FOOTER_BYTES": 8 * 2
}
