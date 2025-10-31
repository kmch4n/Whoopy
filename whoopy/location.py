"""Location management for Whoopy API."""
from .utils import HTTPClient


class Location:
    """Handle location-related API operations."""

    def __init__(self, headers: dict):
        """
        Initialize Location instance.

        Args:
            headers: HTTP headers for API requests
        """
        self.client = HTTPClient(headers)

    def online(self) -> None:
        """Set user status to online."""
        url = 'https://www.wh00.ooo/api/user/online'
        self.client.patch(url)

    def offline(self) -> None:
        """Set user status to offline."""
        url = 'https://www.wh00.ooo/api/user/offline'
        self.client.patch(url)

    def update_location(
        self,
        latitude: str,
        longitude: str,
        battery_level: int,
        battery_status: str,
        stayed_at: str,
        speed: int
    ) -> None:
        """
        Update user location and battery information.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            battery_level: Battery level percentage
            battery_status: Battery status code
            stayed_at: Timestamp of stay
            speed: Speed in km/h
        """
        url = 'https://www.wh00.ooo/api/user/location'
        params = {
            "user_location": {
                "latitude": latitude,
                "longitude": longitude,
                "stayed_at": stayed_at,
                "speed": speed
            },
            "user_battery": {
                "level": battery_level,
                "state": battery_status
            }
        }
        self.client.patch(url, json=params)
