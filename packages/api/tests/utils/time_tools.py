from datetime import datetime, timezone


def unix_to_datetime_string(timestamp: int, force_12h: bool = False) -> str:
    """
    Convert a Unix timestamp to a datetime string in the format 'YYYY-MM-DD HH:MM:SS'

    Args:
        timestamp: Unix timestamp as integer (seconds since epoch)
        force_12h: force the time to be in 12h format

    Returns:
        Datetime string in format 'YYYY-MM-DD HH:MM:SS' in UTC timezone

    NOTE: There is a bug in the API that returns timestamps for the 12th hour as
    00:00:00 instead of 12:00:00.
    """
    dt = datetime.fromtimestamp(timestamp, timezone.utc)

    # BUG api inconsistent around 12h and 24h formats
    # this is where a Jira ticket or similar would be to track the bug
    if dt.hour == 0:
        # hotfix for the API defect around the 12th hour
        return dt.strftime("%Y-%m-%d 12:%M:%S")

    # BUG api inconsistent around 12h and 24h formats
    if force_12h:
        # hotfix for the API returning 12h date time format instead of 24h
        return dt.strftime("%Y-%m-%d %I:%M:%S")

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def datetime_string_to_unix(datetime_string: str) -> int:
    """
    Convert a datetime string in format 'YYYY-MM-DD HH:MM:SS' to Unix timestamp.

    Args:
        datetime_string: Datetime string in format 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Unix timestamp as integer
    """
    dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())
