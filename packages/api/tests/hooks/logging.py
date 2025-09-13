import pytest
import logging
from tests.logging_config import setup_logging


@pytest.fixture(scope="session")
def logger(request) -> logging.Logger:
    """
    Session fixture for the logger, handling pytest-xdist.
    Creates a unique log file for each worker.
    """
    worker_id = "master"
    if hasattr(request.config, "workerinput"):
        worker_id = request.config.workerinput["workerid"]

    # TODO clean up logs dir before test run
    # TODO gather logs from all worker files and merge them into one log file

    return setup_logging(worker_id)
