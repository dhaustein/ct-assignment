from typing import Generator
from api_sdk import ApiClient, Configuration
import pytest

# TODO should be part of config file
BASE_URL = "https://helloacm.com"

@pytest.fixture(scope="session")
def api_client() -> Generator[ApiClient, None, None]:
    """Sessionfixture to create an API client"""
    configuration = Configuration(host=BASE_URL)
    with ApiClient(configuration) as client:
        yield client
