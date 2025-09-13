from packages.frontend.tests.pages.timestamp_page import TimestampConverterPage


def test_convert_timestamp_to_date(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting a Unix timestamp to a date string.
    """
    timestamp_converter_page.navigate()
    timestamp_converter_page.convert_timestamp_to_date("175766100")

    # BUG the resulting date time string should be zero-padded
    assert timestamp_converter_page.get_converted_date() == "1975-07-28 7:55:00"

def test_convert_date_to_timestamp(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting a date string to a Unix timestamp.
    """
    timestamp_converter_page.navigate()
    timestamp_converter_page.convert_date_to_timestamp("2023-01-01 00:00:00")
    assert timestamp_converter_page.get_converted_timestamp() == "1672531200"

def test_invalid_timestamp(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting an invalid timestamp.
    """
    timestamp_converter_page.navigate()
    timestamp_converter_page.convert_timestamp_to_date("invalid")
    assert "NaN" in timestamp_converter_page.get_converted_date()

def test_convert_timestamp_epoch_start(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting zero Unix timestamp (epoch start).
    """
    timestamp_converter_page.navigate()
    timestamp_converter_page.convert_timestamp_to_date("0")

    # BUG the resulting date time string should be zero-padded
    assert timestamp_converter_page.get_converted_date() == "1970-01-01 0:0:00"

def test_convert_timestamp_leap_day(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting a leap day timestamp.
    """
    timestamp_converter_page.navigate()
    timestamp_converter_page.convert_timestamp_to_date("1582934400")

    # BUG the resulting date time string should be zero-padded
    assert timestamp_converter_page.get_converted_date() == "2020-02-29 0:0:00"

def test_invalid_date(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting an invalid date string.
    """
    timestamp_converter_page.navigate()
    timestamp_converter_page.convert_date_to_timestamp("invaliddate")
    assert "NaN" in timestamp_converter_page.get_converted_timestamp()

def test_timestamp_tick(timestamp_converter_page: TimestampConverterPage):
    """
    Test the current timestamp and date being displayed each second.
    """
    pass

def test_convert_timestam_in_different_timezones(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting a Unix timestamp to a date string while in different timezone.
    """
    pass

def test_convert_date_in_different_timezones(timestamp_converter_page: TimestampConverterPage):
    """
    Test converting a date string to a Unix timestamp while in different timezone.
    """
    pass
