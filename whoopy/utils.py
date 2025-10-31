"""Utility functions for HTTP requests and error handling."""
import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Optional


class HTTPClient:
    """HTTP client with common error handling and timeout configuration."""

    def __init__(self, headers: dict, timeout: int = 30):
        """
        Initialize HTTP client.

        Args:
            headers: HTTP headers for requests
            timeout: Request timeout in seconds (default: 30)
        """
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.timeout = timeout

    def _handle_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Execute HTTP request with error handling.

        Args:
            method: HTTP method (GET, POST, PATCH, etc.)
            url: Request URL
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            Exception: If request fails
        """
        kwargs.setdefault('timeout', self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'N/A'
            raise Exception(f"[{status_code}] HTTP error: {http_err}") from http_err
        except RequestException as req_err:
            raise Exception(f"Request failed: {req_err}") from req_err

    def get(self, url: str, **kwargs) -> requests.Response:
        """Execute GET request."""
        return self._handle_request('GET', url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        """Execute PATCH request."""
        return self._handle_request('PATCH', url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """Execute POST request."""
        return self._handle_request('POST', url, **kwargs)
