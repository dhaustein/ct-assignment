from api_sdk import ApiClient, Configuration, TimestampApi
import pytest

BASE_URL = "https://helloacm.com"

@pytest.fixture
def api_client() -> ApiClient:
    """Pytest fixture to create an API client."""
    configuration = Configuration(host=BASE_URL)
    with ApiClient(configuration) as client:
        yield client

@pytest.fixture
def timestamp_api(api_client: ApiClient) -> TimestampApi:
    """Pytest fixture to create a TimestampApi instance."""
    return TimestampApi(api_client)

def test_convert_timestamp_integer(timestamp_api: TimestampApi):
    """
    Test converting a Unix timestamp integer to a date string.
    """
    test_timestamp = 1672531200

    # TODO cached= must be eny empty string (bake this into the wrapper later)
    response = timestamp_api.convert_timestamp(cached="", s=test_timestamp)

    # The API returns a ConvertTimestamp200Response object.
    # The actual data is in `actual_instance`.
    assert response.actual_instance is not None

    # NOTE the datetime should be by default GMT and not affected by the timezone
    assert response.actual_instance == "2023-01-01 12:00:00"

def test_convert_timestamp_string(timestamp_api: TimestampApi):
    """
    Test converting a date string to a Unix timestamp.
    """
    test_date_string = "2023-01-01 00:00:00"
    expected_timestamp = 1672531200

    response = timestamp_api.convert_timestamp(cached="", s=test_date_string)

    assert response.actual_instance is not None
    assert not isinstance(response.actual_instance, bool)
    assert response.actual_instance == expected_timestamp

def test_convert_timestamp_invalid(timestamp_api: TimestampApi):
    """
    Test sending an invalid string to the converter.
    """
    invalid_string = "foo"

    response = timestamp_api.convert_timestamp(cached="", s=invalid_string)
    assert not response.actual_instance
