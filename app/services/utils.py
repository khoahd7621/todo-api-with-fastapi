from uuid import UUID
from datetime import datetime, timezone

from .exception import InvalidInputError

def get_current_utc_time():
    return datetime.now(timezone.utc)


def validate_uuid(id):
    try:
        UUID(id)
    except ValueError:
        raise InvalidInputError("Invalid UUID")