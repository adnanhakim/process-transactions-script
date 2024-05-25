"""
utils.dates
~~~~~~~~~~~~~~

This module contains common date methods.

"""

from datetime import datetime


def to_datetime(datestring: str, dateformat: str) -> datetime:
    """Converts a date string with format dd-MM-yyyy to a datetime object"""
    return datetime.strptime(datestring, dateformat)


def to_datestring(date: datetime) -> str:
    """Converts a datetime object to a date string with format dd-MM-yyyy"""
    if date is None:
        return ""

    return date.strftime("%d-%m-%Y")


def get_timestamp() -> str:
    return datetime.now().time().strftime("%H%M%S")
