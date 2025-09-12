import pytest
from .fixtures.timestamp import TestTimestampApi
from .utils.time_tools import unix_to_datetime_string, datetime_string_to_unix


def test_convert_timestamp_midnight(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a Unix midnight timestamp integer to a date string.
    """
    ts = 1672531200  # 2023-01-01 00:00:00

    res = timestamp_client.convert(timestamp=ts)

    assert res.status_code == 200
    assert res.payload == unix_to_datetime_string(ts)

def test_convert_datetime_midnight(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting a midnight date string to a Unix timestamp.
    """
    dt = "2023-01-01 00:00:00"  # 1672531200

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == datetime_string_to_unix(dt)

def test_convert_one_am(timestamp_client: TestTimestampApi) -> None:
    """
    Test converting 1AM date string to a Unix timestamp.
    """
    dt = "2023-01-01 01:00:00"

    res = timestamp_client.convert(timestamp=dt)

    assert res.status_code == 200
    assert res.payload == datetime_string_to_unix(dt)

def test_convert_timestamp_invalid_string(timestamp_client: TestTimestampApi) -> None:
    """
    Test sending an invalid string to the converter.
    Response should be HTTP 200 but the payload contains only 'false'.
    """
    invalid_string = "foo"

    res = timestamp_client.convert(timestamp=invalid_string)
    assert res.status_code == 200
    assert not res.payload
