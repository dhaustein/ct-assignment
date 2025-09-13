import pytest
from api_sdk import ApiClient, TimestampApi, ApiResponse
from api_sdk.models.convert_timestamp200_response import ConvertTimestamp200Response
from typing import Optional, Mapping, Union, Dict, Any
import logging


class ConvertedRes:
    """
    Wrapper class for easier access to API response data.

    Args:
        api_response (ApiResponse[ConvertTimestamp200Response]): The API response
                                                                object to wrap.
    """

    def __init__(self, api_response: ApiResponse[ConvertTimestamp200Response]) -> None:
        self._response = api_response

    @property
    def status_code(self) -> int:
        """
        Get the HTTP status code of the response.

        Returns:
            int: The HTTP status code
        """
        return self._response.status_code

    @property
    def headers(self) -> Optional[Mapping[str, str]]:
        """
        Get the HTTP headers of the response.

        Returns:
            Optional[Mapping[str, str]]: A mapping of header names to values,
                                        or None if no headers are present.
        """
        return self._response.headers

    @property
    def payload(self) -> Optional[Union[Dict[str, Any], bool, int, str]]:
        """
        Get the response payload as a dictionary.

        Returns:
            Optional[Union[Dict[str, Any], bool, int, str]]: The response data
                                                            converted to a dictionary,
                                                            or None if no data is present.
        """
        return self._response.data.to_dict()

    @property
    def data_obj(self) -> ConvertTimestamp200Response:
        """
        Get the raw response data object.

        Returns:
            ConvertTimestamp200Response: The original response model object.
        """
        return self._response.data

    @property
    def raw_data(self) -> bytes:
        """
        Get the raw response data as bytes.

        Returns:
            bytes: The raw HTTP response body as bytes.
        """
        return self._response.raw_data


class TestTimestampApi(TimestampApi):
    """
    Extended TimestampApi class with additional logging and convenience methods.

    This class extends the base TimestampApi to provide enhanced logging
    capabilities and a simplified interface for timestamp conversion operations
    in test scenarios.

    Args:
        api_client (ApiClient): The API client instance for making HTTP requests.
        logger (logging.Logger): Logger instance for recording API operations.
    """

    def __init__(self, api_client: ApiClient, logger: logging.Logger) -> None:
        super().__init__(api_client)
        self.logger = logger

    def convert(
        self,
        timestamp: int | str,  # TODO should be Datetime instead of plain str?
        cached: str | None = "",
    ) -> ConvertedRes:
        """
        Convert timestamp with enhanced logging and response wrapping.

        Performs timestamp conversion using the underlying API while providing
        detailed logging of the request and response. The response is wrapped
        in a ConvertedRes object for easier access to response data.

        Args:
            timestamp (int | str): The Unix timestamp (integer) or date string
                                  to convert.
            cached (str | None, optional): Enable caching for the conversion.
                                          Defaults to "".

        Returns:
            ConvertedRes: A wrapped response object providing convenient access
                         to the conversion result, status code, headers, and raw data.
        """
        self.logger.info("Converting timestamp: %s", timestamp)

        res = self.convert_timestamp_with_http_info(cached=cached, s=timestamp)

        self.logger.info("Conversion response status: %s", res.status_code)
        self.logger.debug("Conversion response payload: %s", res.data)

        return ConvertedRes(res)


@pytest.fixture(scope="session")
def timestamp_client(api_client: ApiClient, logger: logging.Logger) -> TestTimestampApi:
    """
    Session fixture to create a Timestamp endpoint instance.

    Creates a TestTimestampApi instance that will be shared across all tests
    in the session.

    This fixture also provides an enhanced API client with logging capabilities
    for timestamp conversion operations.

    Args:
        api_client (ApiClient): The base API client instance.
        logger (logging.Logger): Logger instance for recording operations.

    Returns:
        TestTimestampApi: An enhanced timestamp API client instance with
                         logging and convenience methods.
    """
    logger.info("Creating Timestamp API client")
    return TestTimestampApi(api_client, logger)
