"""User management for Whoopy API."""
from typing import Any
from .utils import HTTPClient


class User:
    """Handle user-related API operations."""

    def __init__(self, headers: dict):
        """
        Initialize User instance.

        Args:
            headers: HTTP headers for API requests
        """
        self.client = HTTPClient(headers)

    def find_user(self, user_name: str) -> dict[str, Any]:
        """
        Find user by display name.

        Args:
            user_name: Display name to search for

        Returns:
            User information dictionary

        Raises:
            ValueError: If no user found with the given name
        """
        params = {
            "display_name": user_name
        }
        response = self.client.get(
            'https://www.wh00.ooo/api/friends/search',
            params=params
        )
        data = response.json()
        friends = data.get("friends")
        if not isinstance(friends, list) or len(friends) == 0:
            raise ValueError(f"No user found with name '{user_name}'.")
        return friends[0]

