from typing import Generator
from api_sdk import ApiClient, Configuration
import pytest
import logging

# TODO should be part of config file
BASE_URL = "https://helloacm.com"


@pytest.fixture(scope="session")
def api_client(logger: logging.Logger) -> Generator[ApiClient, None, None]:
    """Sessionfixture to create an API client"""
    logger.info("Creating API client for host: %s", BASE_URL)
    configuration = Configuration(host=BASE_URL)
    with ApiClient(configuration) as client:
        yield client
    logger.info("API client closed")
