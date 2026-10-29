from datetime import datetime


def checkingout_is_open(closes_at: datetime, now: datetime) -> bool:
    """Both arguments must be timezone-aware UTC timestamps."""
    return now < closes_at
