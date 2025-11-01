from enum import Enum, IntEnum


class BatteryState(IntEnum):
    """Enum representing battery states"""
    UNKNOWN = 0
    CHARGING = 1
    FULL = 2
    DISCHARGING = 3


class HttpStatus(IntEnum):
    """Enum representing HTTP status codes"""
    OK = 200
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# Other constants
SPEED_CONVERSION_FACTOR = 3.6  # Conversion factor from km/h to m/s
DEFAULT_BATTERY_LEVEL = 100
DEFAULT_BATTERY_STATE = BatteryState.UNKNOWN
