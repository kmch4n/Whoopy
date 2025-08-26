import requests
from requests.exceptions import HTTPError, RequestException

class Action:
    def __init__(self, headers: dict):
        self.headers = headers

    def online(self) -> None:
        url = 'https://www.wh00.ooo/api/user/online'
        try:
            response = requests.patch(url, headers=self.headers)
            response.raise_for_status()
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'N/A'
            raise Exception(f"[{status_code}] Failed to go online: {http_err}") from http_err
        except RequestException as req_err:
            raise Exception(f"Request failed while trying to go online: {req_err}") from req_err

    def offline(self) -> None:
        url = 'https://www.wh00.ooo/api/user/offline'
        try:
            response = requests.patch(url, headers=self.headers)
            response.raise_for_status()
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'N/A'
            raise Exception(f"[{status_code}] Failed to go offline: {http_err}") from http_err
        except RequestException as req_err:
            raise Exception(f"Request failed while trying to go offline: {req_err}") from req_err

    def update_location(self, latitude: str, longitude: str, battery_level: int , battery_status : str, stayed_at: str , speed: int) -> None:
        url = 'https://www.wh00.ooo/api/user/location'
        params = {
            "user_location" : {
            "latitude" : latitude,
            "longitude" : longitude,
            "stayed_at" : stayed_at,
            "speed" : speed
            },
            "user_battery" : {
            "level" : battery_level,
            "state" : battery_status
            }
        }
        try:
            response = requests.patch(url, headers=self.headers, json=params)
            response.raise_for_status()
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'N/A'
            raise Exception(f"[{status_code}] Failed to update location: {http_err}") from http_err
        except RequestException as req_err:
            raise Exception(f"Request failed while trying to update location: {req_err}") from req_err
