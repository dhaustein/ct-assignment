import pytest
from api_sdk import ApiClient, TimestampApi, ApiResponse
from api_sdk.models import ConvertTimestamp200Response
from typing import Optional, Mapping, Union, Dict, Any
import logging


class ConvertedRes:
    """Wrapper class for easier access to API response data"""

    def __init__(self, api_response: ApiResponse[ConvertTimestamp200Response]):
        self._response = api_response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> Optional[Mapping[str, str]]:
        return self._response.headers

    @property
    def payload(self) -> Optional[Union[Dict[str, Any], bool, int, str]]:
        return self._response.data.to_dict()

    @property
    def data_obj(self) -> ConvertTimestamp200Response:
        return self._response.data

    @property
    def raw_data(self) -> bytes:
        return self._response.raw_data


class TestTimestampApi(TimestampApi):
    def __init__(self, api_client: ApiClient, logger: logging.Logger):
        super().__init__(api_client)
        self.logger = logger

    def convert(
        self,
        timestamp: int | str,  # TODO should be Datetime instead of plain str?
        cached: str | None = ""
        ) -> ConvertedRes:
        """Convert timestamp"""
        self.logger.info("Converting timestamp: %s", timestamp)

        res = self.convert_timestamp_with_http_info(cached=cached, s=timestamp)

        self.logger.info("Conversion response status: %s", res.status_code)
        self.logger.debug("Conversion response payload: %s", res.data)

        return ConvertedRes(res)

@pytest.fixture(scope="session")
def timestamp_client(api_client: ApiClient, logger: logging.Logger) -> TestTimestampApi:
    """Session fixture to create a Timestamp endpoint instance"""
    logger.info("Creating Timestamp API client")
    return TestTimestampApi(api_client, logger)
