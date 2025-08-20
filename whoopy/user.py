import json
import requests
from requests.exceptions import HTTPError, RequestException

class User:
    def __init__(self, headers: dict):
        self.headers = headers

    def find_user(self, user_name: str) -> json:
        params = {
            "display_name" : user_name
        }
        try:
            response = requests.get(f'https://www.wh00.ooo/api/friends/search', params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            friends = data.get("friends")
            if not isinstance(friends, list) or len(friends) == 0:
                raise ValueError(f"No user found with name '{user_name}'.")
            return friends[0]
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'N/A'
            raise Exception(f"[{status_code}] Failed to get user: {http_err}") from http_err
        except RequestException as req_err:
            raise Exception(f"Request failed while getting user: {req_err}") from req_err

