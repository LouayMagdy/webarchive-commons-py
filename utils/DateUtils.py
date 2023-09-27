import datetime
import math
import pytz
import locale
import threading
import time


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
LAST_UNIQUE_NOW14 = 0
LAST_TIMESTAMP14 = ""
UNIQUE_14METHOD_LOCK = threading.Lock()

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


def parse_12_digit_date(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, "%Y%m%d%H%M")


def parse_14_digit_date(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")


def parse_17_digit_date(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date + "000", "%Y%m%d%H%M%S%f")


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
        if not (d.startswith('19') or d.startswith('20')):
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


def get_seconds_since_epoch(date_str: str) -> datetime.datetime:
    if len(date_str) < 14:
        if len(date_str) < 10 and len(date_str) % 2:
            raise Exception(f"Must have year, month, date, hour or second granularity: {date_str}")
        if len(date_str) == 4:  # has the year only --> add first month and first date
            date_str += "01010000"
        if len(date_str) == 6:  # has the year & month --> add first date
            date_str += "010000"
        if len(date_str) < 14:
            date_str += ("0" * (14 - len(date_str)))
    return parse_14_digit_date(date_str)


def seconds_since_epoch(date_str: str) -> str:
    res = str(int(get_seconds_since_epoch(date_str).timestamp()))
    return ('0' * (MAX_INT_CHAR_WIDTH - len(res))) + res


def double_to_string(val, max_fraction_digits, min_fraction_digits=0):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    f = '{:,.{max_fraction_digits}f}'.format(val, max_fraction_digits=max_fraction_digits)
    if min_fraction_digits > 0:
        f = f.rstrip('0').rstrip('.')
        if '.' not in f:
            f += '.'
        f += '0' * (min_fraction_digits - len(f.split('.')[1]))
    return f


def format_bytes_for_display(amount: int) -> str:
    display_amount, unit_power_of_1024 = amount, 0
    if amount <= 0:
        return "0 B"
    while display_amount >= 1024 and unit_power_of_1024 < 4:
        display_amount /= 1024
        unit_power_of_1024 += 1
    units = [" B", " KiB", " MiB", " GiB", " TiB"]
    fraction_digits = 1 if display_amount < 10 else 0  # for small values
    return double_to_string(display_amount, fraction_digits, fraction_digits) + units[unit_power_of_1024]


def format_ms_to_conventional(time: int, unit_count: int = 5):
    if unit_count < 1:
        unit_count = 5
    if time == 0:
        return "0ms"
    result = ""
    if time < 0:
        result += '-'
    abs_time, thresholds, units = math.fabs(time), [DAY_IN_MS, HOUR_IN_MS, 60000, 1000, 1], ["d", "h", "m", "s", "ms"]
    for i in range(len(thresholds)):
        if abs_time > thresholds[i]:
            result += str(int(abs_time / thresholds[i])) + units[i]
            abs_time %= thresholds[i]
            unit_count -= 1
        if not unit_count:
            break
    return result


def get_unique_14_digit_date() -> str:
    with UNIQUE_14METHOD_LOCK:
        global LAST_UNIQUE_NOW14
        global LAST_TIMESTAMP14
        curr_time_millis = round(time.time() * 1000)
        effective_now = max(curr_time_millis, LAST_UNIQUE_NOW14 + 1)
        candidate = get_14_digit_date(ms=effective_now)
        while candidate == LAST_TIMESTAMP14:
            effective_now += 1000
            candidate = get_14_digit_date(ms=effective_now)
        LAST_UNIQUE_NOW14, LAST_TIMESTAMP14 = effective_now, candidate
        return candidate


# now = datetime.datetime.now()
# print(time_stamp_12.format(now), get_12_digit_date(now))
# print(time_stamp_14.format(now), get_14_digit_date(now))
# print(time_stamp_17.format(now), get_17_digit_date(now))
# print(time_stamp_17ISO8601Z.format(now), get_log17_digit_date(now))
# print(time_stamp_14ISO8601Z.format(now), get_log14_digit_date(now))
# print(parse_12_digit_date('202309261432'))
# print(parse_14_digit_date('20230926143251'))
# print(parse_17_digit_date('20230926143251458'))
# print(seconds_since_epoch('19700105'), MAX_INT_CHAR_WIDTH)
# print(double_to_string(3.14, 6,4))
# print(format_bytes_for_display(1025), format_bytes_for_display(51200 * 1024 * 1024))
# print(format_ms_to_conventional(-147258369, 4))
# print(get_unique_14_digit_date())
