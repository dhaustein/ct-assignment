import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_LEVEL = "DEBUG"
LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s @ %(module)s:%(lineno)d]: %(message)s"

def setup_logging(worker_id: str = "master") -> logging.Logger:
    """
    Setup logging for a specific worker so it works with pytest-xdist.

    Args:
        worker_id: The ID of the pytest-xdist worker.

    Returns:
        A configured logger instance.
    """
    log_filename = f"api_test_{worker_id}.log"
    logger = logging.getLogger(f"api_test_{worker_id}")

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(LOG_LEVEL)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(LOG_DIR / log_filename, mode="w")
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
