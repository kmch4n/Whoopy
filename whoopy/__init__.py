"""Whoopy API client for location and user management."""
from typing import Any
import logging
import json
import os
from pathlib import Path

from .location import Location
from .user import User
from .profile import Profile

logger = logging.getLogger(__name__)


class Whoo:
    """Main client for Whoopy API."""

    def __init__(self, token: str, header_file: str = 'header.json'):
        """
        Initialize Whoopy client.

        Args:
            token: API authentication token
            header_file: Path to header configuration file (default: 'header.json')

        Raises:
            FileNotFoundError: If header file doesn't exist
            json.JSONDecodeError: If header file contains invalid JSON
        """
        self.token = token

        # Load headers with error handling
        header_path = Path(header_file)
        if not header_path.exists():
            raise FileNotFoundError(
                f"Header file not found: {header_file}. "
                f"Please ensure the file exists in the current directory."
            )

        try:
            with open(header_path, 'r', encoding='utf-8') as f:
                headers: dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in header file: {header_file}",
                e.doc,
                e.pos
            ) from e

        headers["Authorization"] = f"Bearer {token}"

        # Initialize API components
        self.location = Location(headers)
        self.user = User(headers)
        self.profile = Profile(headers)

    def log(self, text: str) -> None:
        """
        Log informational message.

        Args:
            text: Message to log
        """
        logger.info(text)

    def online(self) -> None:
        """Set user status to online."""
        return self.location.online()

    def offline(self) -> None:
        """Set user status to offline."""
        return self.location.offline()

    def find_user(self, user_name: str) -> dict[str, Any]:
        """
        Find user by display name.

        Args:
            user_name: Display name to search for

        Returns:
            User information dictionary
        """
        return self.user.find_user(user_name)

    def update_location(
        self,
        latitude: str,
        longitude: str,
        battery_level: int = 100,
        battery_status: str = "2",
        stayed_at: str = '1970-01-01 05:00:32 +0000',
        speed: int = 0
    ) -> None:
        """
        Update user location and battery information.

        Args:
            latitude: 緯度 (Latitude)
            longitude: 経度 (Longitude)
            battery_level: バッテリー残量 (%) (Battery level percentage, default: 100)
            battery_status: バッテリー状態 (Battery status, default: "2")
                           [0,1,2,3] = [不明、充電中、充電完了、充電していない]
                           [0,1,2,3] = [Unknown, Charging, Charged, Not charging]
            stayed_at: 滞在時間 (Stay timestamp, default: '1970-01-01 05:00:32 +0000')
            speed: 速度 (km/h) (Speed in km/h, default: 0)
        """
        return self.location.update_location(
            latitude,
            longitude,
            battery_level,
            battery_status,
            stayed_at,
            speed
        )