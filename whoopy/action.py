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

    def update_location(self, latitude: str, longitude: str, stayed_at: str = '1970-01-01 05:00:32 +0000', ):
        pass
