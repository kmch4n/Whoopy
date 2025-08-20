from typing import Any
import logging
import json

from .action import Action
from .user import User

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Whoo:
    def __init__(self, token: str):
        self.token = token
        with open('header.json','r') as f:
            headers: dict[str, Any] = json.load(f)
        headers["Authorization"] = f"Bearer {token}"
        self.action = Action(headers)
        self.user = User(headers)

    def log(self, text: str) -> None:
        logger.info(text)

    def online(self) -> str:
        return self.action.online()

    def find_user(self, user_name: str) -> json:
        return self.user.find_user(user_name)