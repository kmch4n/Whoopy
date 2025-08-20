import requests
from requests.exceptions import HTTPError, RequestException

class Profile:
    def __init__(self, headers: dict):
        self.headers = headers

    def update_profile(self, name: str = None, profile_image: str = None, username: str = None) -> None:
        url = "https://www.wh00.ooo/api/user"
        params = {
            "display_name": name,
            "profile_image": profile_image,
            "username": username
        }
        try:
            response = requests.patch(url, headers=self.headers, json=params)
            response.raise_for_status()
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'N/A'
            raise Exception(f"[{status_code}] Failed to update profile: {http_err}") from http_err
        except RequestException as req_err:
            raise Exception(f"Request failed while updating profile: {req_err}") from req_err
