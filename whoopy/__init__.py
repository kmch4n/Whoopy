from typing import Any
import logging
import json

from .location import Location
from .user import User

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Whoo:
    def __init__(self, token: str):
        self.token = token
        with open('header.json','r') as f:
            headers: dict[str, Any] = json.load(f)
        headers["Authorization"] = f"Bearer {token}"
        self.location = Location(headers)
        self.user = User(headers)

    def log(self, text: str) -> None:
        logger.info(text)

    # Location
    def online(self) -> str:
        return self.location.online()

    def find_user(self, user_name: str) -> json:
        return self.user.find_user(user_name)

    def update_location(self, latitude: str, longitude: str, battery_level: int = 100, battery_status: str = 2, stayed_at: str = '1970-01-01 05:00:32 +0000', speed: int = 0) -> None:
        '''
        latitude : 緯度
        longitude : 経度
        battery_level : バッテリー残量 (%)
        battery_status : バッテリー状態 [0,1,2,3] = [不明、充電中、充電完了、充電していない]
        stayed_at : 滞在時間
        speed : 速度 (km/h)
        '''
        return self.location.update_location(latitude, longitude, battery_level, battery_status, stayed_at, speed)