import pytest
from .fixtures.timestamp import TestTimestampApi
from .utils.time_tools import unix_to_datetime_string, datetime_string_to_unix

def test_convert_timestamp_midnight(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a Unix midnight timestamp to a date string.
    """
    ts = 1672531200  # 2023-01-01 00:00:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_noon(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a Unix noon timestamp to a date string.
    """
    ts = 1672574400  # 2023-01-01 12:00:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_regular_time(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a regular time Unix timestamp to a date string.
    """
    ts = 1672603800  # 2023-01-01 20:10:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts, force_12h=True)

def test_convert_timestamp_one_second_after_midnight(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a timestamp one second after midnight.
    """
    ts = 1672531201  # 2023-01-01 00:00:01 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_leap_day_midnight(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a leap day midnight timestamp.
    """
    ts = 1582934400  # 2020-02-29 00:00:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts, force_12h=True)

def test_convert_timestamp_end_of_year(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a timestamp at the end of a year.
    """
    ts = 1672531199  # 2022-12-31 23:59:59 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts, force_12h=True)

def test_convert_timestamp_epoch_start(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting the zero Unix timestamp (epoch start).
    """
    ts = 0  # 1970-01-01 00:00:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_year_2038(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a timestamp around the Year 2038 problem.
    """
    ts = 2147483647  # 2038-01-19 03:14:07 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_pre_epoch(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a negative (pre-epoch) timestamp.
    """
    ts = -2208988800  # 1900-01-01 00:00:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_future(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a timestamp far in the future.
    """
    ts = 32503680000  # 3000-01-01 00:00:00 UTC

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_timestamp_as_string(timestamp_client: TestTimestampApi) -> None:
    """
    Test passing a timestamp as a string.
    """
    ts_int = 1672531200
    ts_str = "1672531200"

    res = timestamp_client.convert(timestamp=ts_str)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts_int)

def test_convert_string_midnight(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a midnight date string to a Unix timestamp.
    """
    dt = "2023-01-01 00:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == datetime_string_to_unix(dt)

def test_convert_string_noon(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a noon datetime string.
    """
    dt = "2023-01-01 12:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == datetime_string_to_unix(dt)

def test_convert_string_leap_day(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a leap day datetime string.
    """
    dt = "2020-02-29 12:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == datetime_string_to_unix(dt)

def test_convert_string_invalid_value(timestamp_client: TestTimestampApi) -> None:
    """
    Test sending an invalid string to the converter.
    """
    res = timestamp_client.convert(timestamp="foo")

    assert res.status_code == 200
    assert not res.payload

def test_convert_string_non_existing_leap_day(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a non-existing Feb 29 on a non-leap year.
    Should jump to 2023-03-01 00:00:00 UTC.
    """
    dt = "2023-02-29 00:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == 1677628800

def test_convert_string_single_digit_date(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a string with single-digit month/day.
    """
    dt = "2023-1-1 12:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == datetime_string_to_unix(dt)

def test_convert_string_alternative_format(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a string with an alternative format.
    """
    dt = "2008/03/04 07:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == 1204614000

def test_convert_string_missing_secs(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting an incomplete datetime string (missing seconds).
    """
    dt = "2023-04-14 14:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == 1681480800

def test_convert_string_with_timezone(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a string that includes timezone information.
    The conversion should ignore timezone.
    """
    dt = "1991-10-01 03:00:00+01:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == 686282400  # 1991-10-01 2:00:00

def test_convert_string_12_hour_format(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a string with AM/PM.
    The conversion should ignore AM/PM.
    """
    dt = "2001-12-05 3:00:00 PM"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == 1007564400

def test_convert_string_unicode(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a string with unicode characters.
    """
    dt = "你好世界"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert not res.payload

def test_convert_empty_string(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting an empty string.
    """
    res = timestamp_client.convert(timestamp="")

    assert res.status_code == 200
    assert not res.payload

def test_convert_float_timestamp(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a float timestamp.
    The conversion ignore the fractional part.
    """
    ts = 1308843000.3

    res = timestamp_client.convert(timestamp=ts)  # type: ignore[arg-type]

    assert res.status_code == 200
    assert res.payload == "2011-06-23 03:30:00"

def test_convert_boolean_input(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a boolean value.
    """
    res = timestamp_client.convert(timestamp=True)

    assert res.status_code == 200
    assert not res.payload
