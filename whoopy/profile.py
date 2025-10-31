"""Profile management for Whoopy API."""
from typing import Optional
from .utils import HTTPClient


class Profile:
    """Handle profile-related API operations."""

    def __init__(self, headers: dict):
        """
        Initialize Profile instance.

        Args:
            headers: HTTP headers for API requests
        """
        self.client = HTTPClient(headers)

    def update_profile(
        self,
        name: Optional[str] = None,
        profile_image: Optional[str] = None,
        username: Optional[str] = None
    ) -> None:
        """
        Update user profile information.

        Args:
            name: Display name
            profile_image: Profile image URL or path
            username: Username

        Raises:
            ValueError: If all parameters are None
        """
        if name is None and profile_image is None and username is None:
            raise ValueError("At least one parameter must be provided")

        url = "https://www.wh00.ooo/api/user"
        params = {}
        if name is not None:
            params["display_name"] = name
        if profile_image is not None:
            params["profile_image"] = profile_image
        if username is not None:
            params["username"] = username

        self.client.patch(url, json=params)
