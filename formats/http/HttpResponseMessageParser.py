import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from formats.http.HttpMessageParser import HttpMessageParser
from formats.http.HttpResponseMessage import HttpResponseMessage
from formats.http.HttpResponseMessageObserver import HttpResponseMessageObserver
from formats.http.HttpParseException import HttpParseException
from formats.http.HttpConstants import HttpConstants


class HttpResponseMessageParser(HttpMessageParser):
    def __init__(self) -> None:
        super().__init__()
        self.max_bytes = 1024 * 128
        self.strict = False

    def parse_status_strict(self, buffer: bytearray, start: int, length: int) -> int:
        parsed_status = 0
        try:
            test_status = int(buffer[start: start + length].decode('utf-8'))
            if 100 <= test_status < 600:
                parsed_status = test_status
        except ValueError:
            test_status = 0  # dummy assignment
        if parsed_status == -1:
            raise HttpParseException("Bad status code in Response Message")
        return parsed_status

    def parse_status_lax(self, buffer: bytearray, start: int, length: int) -> int:
        parsed_status = HttpConstants.get('STATUS_UNK')
        try:
            test_status = int(buffer[start: start + length].decode('utf-8'))
            if 100 <= test_status < 600:
                parsed_status = test_status
        except ValueError:
            test_status = 0  # dummy assignment
        return parsed_status

    def parse_message(self, input_stream) -> HttpResponseMessage:
        message = HttpResponseMessage()
        self.parse(message, input_stream)
        return message

    def parse(self, obs: HttpResponseMessageObserver, input_stream=None, buffer: bytearray = None,
              len: int = None) -> int:
        if input_stream:
            bytes_read = 0
            buf = bytearray(self.max_bytes)
            while bytes_read < self.max_bytes:
                i = input_stream.read(1)
                if i == b'':
                    if self.strict:
                        raise HttpParseException("EOF before CRLF")
                    obs.message_corrupt()
                    return bytes_read
                b = i[0]
                if b > 127:
                    if self.strict:
                        raise HttpParseException("Non ASCII byte in message")
                    obs.message_corrupt()
                    return bytes_read
                b &= 0xFF
                buf[bytes_read] = b
                bytes_read += 1
                if b == HttpConstants.get('LF'):
                    if self.strict:
                        bytes_read -= 1
                    return self.parse(obs=obs, buffer=buf, len=bytes_read)
            raise HttpParseException("Response Message too long")
        elif buffer:
            if self.strict:
                return self.parse_strict(obs=obs, buffer=buffer, len=len)
            return self.parse_lax(obs=obs, buffer=buffer, len=len)

    def parse_strict(self, obs: HttpResponseMessageObserver, buffer: bytearray, len: int) -> int:
        if buffer[len - 1] != HttpConstants.get('CR'):
            obs.message_corrupt()
            raise HttpParseException("Response Message missing CRLF")
        version, status, reason = HttpConstants.get('VERSION_0'), 0, HttpConstants.get("REASON_UNK")
        idx, version_start, version_length, status_start, status_length = 0, 0, 0, -1, 0
        while idx < len:
            if buffer[idx] != HttpConstants.get("SP"):  # has not found space = still in the same field
                if status_start == -1:  # detecting version
                    version_length += 1
                else:  # detecting reason
                    status_length += 1

            else:
                if status_start == -1:  # status not yet detected as version was being detected
                    status_start = idx + 1
                else:  # everything have been detected
                    break
            idx += 1

        if idx == len:
            obs.message_corrupt()
            raise HttpParseException("Response Message Missing Fields")
        version = self.parse_version_strict(buffer, version_start, version_length)
        status = self.parse_status_strict(buffer=buffer, start=status_start, length=status_length)
        reason = buffer[idx + 1: len].decode('utf-8')
        obs.message_parsed(version, status, reason, len)
        return len

    def parse_lax(self, obs: HttpResponseMessageObserver, buffer: bytearray, len: int) -> int:
        version, status, reason = HttpConstants.get('VERSION_0'), 0, HttpConstants.get("REASON_UNK")
        idx, version_start, version_length, status_start, status_length, buffer_end = 0, -1, 0, -1, 0, len - 1
        if len > 2 and buffer[len - 2] == HttpConstants.get('CR'):  # some tolerance in the position of CR
            buffer_end -= 1
        while idx < buffer_end:  # Skipping Leading Spaces
            if buffer[idx] != HttpConstants.get('SP'):
                break
            idx += 1
        version_start = idx
        while idx < buffer_end:
            if buffer[idx] != HttpConstants.get('SP'):  # has not found a space = still on the same field
                if status_start == -1:  # detecting version
                    version_length += 1
                else:  # detecting reason
                    status_length += 1
            else:
                if status_start == -1:
                    status_start = idx + 1
                else:
                    break
            idx += 1
        if idx < buffer_end:  # All fields have been found
            version = self.parse_version_lax(buffer, version_start, version_length)
            status = self.parse_status_lax(buffer=buffer, start=status_start, length=status_length)
            idx += 1
            reason_len = buffer_end - idx
            if reason_len > 0:
                reason = buffer[idx: idx + reason_len].decode('utf-8')
        else:
            if version_length > 0:
                version = self.parse_version_lax(buffer, version_start, version_length)
            if status_length > 0:
                status = self.parse_status_lax(buffer=buffer, start=status_start, length=status_length)
        obs.message_parsed(version, status, reason, len)
        return len


# parser = HttpResponseMessageParser()
# # parser.strict = True
# obs = HttpResponseMessage()
# data = b'    HTTP/1.0 200 OK\r\r'
# parser.parse(obs=obs, buffer=bytearray(data), len=len(bytearray(data)))
# print(obs.version)
# print(obs.status)
# print(obs.reason)
# print(obs.to_string())
#
#
# parser = HttpResponseMessageParser()
# parser.strict = True
# obs = HttpResponseMessage()
# data = b'HTTP/1.1 500 BAD REQUEST\r'
# parser.parse(obs=obs, buffer=bytearray(data), len=len(bytearray(data)))
# print(obs.version)
# print(obs.status)
# print(obs.reason)
# print(obs.to_string())
