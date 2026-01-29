from datetime import datetime, timezone

def dt_to_ms(dt: datetime) -> int:
    """Convert a datetime object to milliseconds since epoch."""
    return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

def ms_to_dt(ms: int) -> datetime:
    """Convert milliseconds since epoch to a datetime object."""
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)

def get_current_milis() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)