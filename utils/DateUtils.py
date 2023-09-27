import datetime
import threading
import pytz


def thread_local_date_format(pattern, pad: int = 0, add_z: bool = False):
    def create_format(date: datetime.datetime):
        date = date.astimezone(pytz.timezone('GMT')).strftime(pattern)
        formatted_date = date[:-pad] if pad else date[:]
        if add_z:
            formatted_date = formatted_date + 'Z'
        return date if len(formatted_date) == 0 else formatted_date

    return create_format


VERSION = '0.1'
DEFAULT_PAD_CHAR = ' '
HOUR_IN_MS = 60 * 60 * 1000
DAY_IN_MS = 24 * HOUR_IN_MS
MAX_INT_CHAR_WIDTH = len(str(1 << 32 - 1))

time_stamp_RFC1123 = threading.local()
time_stamp_RFC1123.format = thread_local_date_format("%a, %d %b %Y %H:%M:%S %Z")

time_stamp_12 = threading.local()
time_stamp_12.format = thread_local_date_format("%Y%m%d%H%M")

time_stamp_14 = threading.local()
time_stamp_14.format = thread_local_date_format("%Y%m%d%H%M%S")

time_stamp_17 = threading.local()
time_stamp_17.format = thread_local_date_format("%Y%m%d%H%M%S%f", 3)

time_stamp_17ISO8601Z = threading.local()
time_stamp_17ISO8601Z.format = thread_local_date_format("%Y-%m-%dT%H:%M:%S.%f", 3, True)

time_stamp_14ISO8601Z = threading.local()
time_stamp_14ISO8601Z.format = thread_local_date_format("%Y-%m-%dT%H:%M:%S", add_z=True)


def get_rfc1123_date(date: datetime.datetime) -> str:
    return time_stamp_RFC1123.format(date)


def get_17_digit_date(date: datetime.datetime = datetime.datetime.now(), ms: int = None) -> str:
    if ms:
        return get_17_digit_date(datetime.datetime.fromtimestamp(ms / 1000.0))
    return time_stamp_17.format(date)


def get_14_digit_date(date: datetime.datetime = datetime.datetime.now(), ms: int = None) -> str:
    if ms:
        return get_14_digit_date(datetime.datetime.fromtimestamp(ms / 1000.0))
    return time_stamp_14.format(date)


def get_12_digit_date(date: datetime.datetime = datetime.datetime.now(), ms: int = None) -> str:
    if ms:
        return get_12_digit_date(datetime.datetime.fromtimestamp(ms / 1000.0))
    return time_stamp_12.format(date)


def get_log17_digit_date(date: datetime.datetime = datetime.datetime.now(), ms: int = None) -> str:
    if ms:
        return get_log17_digit_date(datetime.datetime.fromtimestamp(ms / 1000.0))
    return time_stamp_17ISO8601Z.format(date)


def get_log14_digit_date(date: datetime.datetime = datetime.datetime.now(), ms: int = None) -> str:
    if ms:
        return get_log14_digit_date(datetime.datetime.fromtimestamp(ms / 1000.0))
    return time_stamp_14ISO8601Z.format(date)


def get_date(d: str) -> datetime.datetime:
    date = None
    if d is None:
        raise Exception("Passed date is null")
    if len(d) == 14:
        date = parse_14_digit_date(d)
    elif len(d) == 17:
        date = parse_17_digit_date(d)
    elif len(d) == 12:
        date = parse_12_digit_date(d)
    elif 0 <= len(d) < 4:
        raise Exception(f"Date string must at least contain a year:{d}{len(d)}")
    else:
        if not(d.startswith('19') or d.startswith('20')):
            raise Exception(f"Unrecognized century: {d}", 0)
        if len(d) < 8 and (len(d) % 2):
            raise Exception(f"Incomplete month/date: {d}", len(d))
        for i in range(len(d), 8, 2):
            d += "01"
        if len(d) < 12:
            for i in range(len(d), 12):
                d += "0"
        date = parse_12_digit_date(d)
        return date


now = datetime.datetime.now()
print(time_stamp_RFC1123.format(now), get_rfc1123_date(now))
print(time_stamp_12.format(now), get_12_digit_date(now))
print(time_stamp_14.format(now), get_14_digit_date(now))
print(time_stamp_17.format(now), get_17_digit_date(now))
print(time_stamp_17ISO8601Z.format(now), get_log17_digit_date(now))
print(time_stamp_14ISO8601Z.format(now), get_log14_digit_date(now))
