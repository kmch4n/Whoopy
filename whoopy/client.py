import requests
from uuid import uuid4
from typing import Dict, Optional

from .enums import BatteryState, HttpStatus, SPEED_CONVERSION_FACTOR, DEFAULT_BATTERY_LEVEL, DEFAULT_BATTERY_STATE


class Whoopy:
    """Whoopy class for Whoo API"""

    def __init__(self, access_token=None, verbose=True, email=None, password=None):
        """
        Initialize Whoopy

        Args:
            access_token: Access token (optional)
            verbose: Display login success message
            email: Email address (use with password)
            password: Password (use with email)
        """
        self.base = 'https://www.wh00.ooo/'
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'app.whoo/0.13.4 iOS/17.0',
            'Accept-Language': 'ja-JP',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        # Login with email/password
        if access_token is None and email and password:
            access_token = self.email_login(email, password)["access_token"]

        # Token authentication
        if access_token:
            self.headers["Authorization"] = f"Bearer {access_token}"
            url = f'{self.base}api/my'
            response = requests.get(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                self.token = True
                if verbose:
                    print("Login successful!")
                return
            else:
                raise Exception(f'Request Error[{response.status_code}] (auth)')
        else:
            self.token = None


    ##############  Account Settings   ##############
    def email_login(self, email, password):
        """
        Login with email address and password

        Args:
            email: Email address
            password: Password

        Returns:
            Dict: Login information (includes access_token)
        """
        url = f'{self.base}api/email/login'
        data = {
            'email': email,
            'password': password
        }
        response = requests.post(url, headers=self.headers, data=data)
        if response.status_code == HttpStatus.OK:
            access_token = response.json()["access_token"]
            self.headers["Authorization"] = f"Bearer {access_token}"
            return response.json()
        else:
            raise Exception(f'Request Error[{response.status_code}] (email login)')

    def create_account(self, email, password, name, profile_image, username, location=None):
        """
        Create a new account

        Args:
            email: Email address
            password: Password
            name: Display name
            profile_image: Profile image URL
            username: Username
            location: Location information (optional, dict with latitude/longitude)

        Returns:
            Dict: Account information
        """
        url = f'{self.base}api/email/users'
        data = {
            'user[email]': email,
            'user[password]': password,
            'user[display_name]': name,
            'user[profile_image]': profile_image,
            'user[username]': username
        }
        response = requests.post(url, headers=self.headers, data=data)

        if response.status_code != HttpStatus.OK:
            raise Exception(f'Request Error[{response.status_code}] (account create)')

        if location is None:
            return response.json()

        # Set location information
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'app.whoo/0.13.4 iOS/17.0',
            'Authorization': f"Bearer {response.json()['access_token']}",
            'Accept-Language': 'ja-JP',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        data = {
            "user_location[latitude]": str(location["latitude"]),
            "user_location[longitude]": str(location["longitude"]),
            "user_location[speed]": 0,
            "user_battery[level]": DEFAULT_BATTERY_LEVEL / 100,
            "user_battery[state]": BatteryState.CHARGING
        }
        url = self.base + 'api/user/location'
        response1 = requests.patch(url, headers=headers, data=data)
        return response.json()

    def update_account(self, name=None, profile_image=None, username=None):
        """
        Update account information

        Args:
            name: Display name (optional)
            profile_image: Profile image URL (optional)
            username: Username (optional)

        Returns:
            Dict: Updated account information
        """
        url = f'{self.base}api/user'
        data = {
            'user[display_name]': name,
            'user[profile_image]': profile_image,
            'user[username]': username
        }
        response = requests.patch(url, headers=self.headers, data=data)
        if response.status_code == HttpStatus.OK:
            return response.json()
        else:
            raise Exception(f'Request Error[{response.status_code}] (account update)')

    def delete_account(self, alert=True):
        """
        Delete account

        Args:
            alert: Show confirmation message

        Returns:
            str: 'Success' or 'Cancel'
        """
        if not self.token:
            raise Exception('Message: Token is required.')

        if alert:
            res = input('Are you sure? (y/n): ')
            if res != 'y':
                return 'Cancel'

        url = f'{self.base}api/user'
        response = requests.delete(url, headers=self.headers)

        if response.status_code != HttpStatus.NO_CONTENT:
            raise Exception(f'Request Error[{response.status_code}] (account delete)')

        return 'Success'


    ##############  Background Processing   ##############
    def info(self):
        """
        Get current user information

        Returns:
            Dict: User information
        """
        if self.token:
            url = f'{self.base}api/my'
            response = requests.get(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (account info)')
        else:
            raise Exception('Message: Token is required.')

    def get_requested(self):
        """
        Get friend requests

        Returns:
            Dict: Friend request information
        """
        if self.token:
            url = f'{self.base}api/friends/requested'
            response = requests.get(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (get requested)')
        else:
            raise Exception('Message: Token is required.')

    def get_friends(self):
        """
        Get friends list

        Returns:
            Dict: Friends list
        """
        if self.token:
            url = f'{self.base}api/friends'
            response = requests.get(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (get my friends)')
        else:
            raise Exception('Message: Token is required.')

    def get_user(self, user_id, friends=False):
        """
        Get specific user information

        Args:
            user_id: User ID
            friends: Also get friends list

        Returns:
            Dict: User information
        """
        if not self.token:
            raise Exception('Message: Token is required.')

        url = f'{self.base}api/v2/users/{user_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code != HttpStatus.OK:
            raise Exception(f'Request Error[{response.status_code}] (get about user info)')

        js = response.json()

        if not friends:
            del js["friends"], js["next_page"]
            return js

        if not js["next_page"]:
            return js

        # Get all friends with pagination
        js["friends"] = []
        for i in range(js["next_page"]):
            url = f'{self.base}api/v2/users/{user_id}/friends?page={i + 1}'
            response = requests.get(url, headers=self.headers)

            if response.status_code != HttpStatus.OK:
                raise Exception(f'Request Error[{response.status_code}] (get friends info)')

            js["friends"] += response.json()["friends"]

        js["next_page"] = None
        return js

    def find_user(self, user_name):
        """
        Search for user by display name

        Args:
            user_name: Display name to search for

        Returns:
            Dict: User information (first match)
        """
        if not self.token:
            raise Exception('Message: Token is required.')

        params = {
            "display_name": user_name
        }
        url = f'{self.base}api/friends/search'
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code != HttpStatus.OK:
            raise Exception(f'Request Error[{response.status_code}] (find user)')

        data = response.json()
        friends = data.get("friends")
        if not isinstance(friends, list) or len(friends) == 0:
            raise ValueError(f"No user found with name '{user_name}'.")

        return friends[0]

    def reacquire_location(self, user_id):
        """
        Send location request to user

        Args:
            user_id: User ID

        Returns:
            Dict: Response information
        """
        if self.token:
            url = self.base + f'api/users/{user_id}/location_request'
            response = requests.get(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (send location request)')
        else:
            raise Exception('Message: Token is required.')

    def update_location(self, location: Dict, level: int = DEFAULT_BATTERY_LEVEL,
                       state: BatteryState = DEFAULT_BATTERY_STATE,
                       speed: float = 0.0, stayed_at: Optional[str] = None,
                       horizontal_accuracy: Optional[float] = None) -> Dict:
        """
        Update user's location information

        Args:
            location: Location dictionary (includes latitude, longitude)
            level: Battery level (0-100). Default is 100
            state: Battery state (BatteryState). Default is 0 (unknown)
            speed: Speed (km/h). Default is 0.0
            stayed_at: Stay time. Optional
            horizontal_accuracy: Horizontal accuracy. Optional

        Returns:
            Dict: Update result
        """
        if self.token:
            url = f'{self.base}api/user/location'
            data = {
                "user_location[latitude]": str(location["latitude"]),
                "user_location[longitude]": str(location["longitude"]),
                "user_location[speed]": str(speed / SPEED_CONVERSION_FACTOR),
                "user_battery[level]": str(level / 100),
                "user_battery[state]": str(state.value)
            }
            if horizontal_accuracy:
                data["user_location[horizontal_accuracy]"] = str(horizontal_accuracy)
            if stayed_at:
                data["user_location[stayed_at]"] = str(stayed_at)
            response = requests.patch(url, headers=self.headers, data=data)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (post location)')
        else:
            raise Exception('Message: Token is required.')

    def get_locations(self, user_id=None):
        """
        Get friends' location information

        Args:
            user_id: Filter by specific user ID (optional)

        Returns:
            Dict: Location information (with Google Maps links)
        """
        if not self.token:
            raise Exception('Message: Token is required.')

        url = self.base + 'api/locations'
        response = requests.get(url, headers=self.headers)

        if response.status_code != HttpStatus.OK:
            raise Exception(f'Request Error[{response.status_code}] (get locations)')

        js = {}
        for loc in response.json()['locations']:
            name = loc['user']['username']
            del loc['user']['username']

            if user_id and user_id != loc['user']['id']:
                continue

            loc["map"] = f"https://maps.google.com/maps?q={loc['latitude']},{loc['longitude']}&t=k&z=24"
            loc['pano'] = f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={loc['latitude']},{loc['longitude']}'
            js[name] = loc

        return js

    def online(self):
        """
        Go online

        Returns:
            Dict: Response information
        """
        if self.token:
            url = self.base + f'api/user/online'
            response = requests.patch(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (online)')
        else:
            raise Exception('Message: Token is required.')

    def offline(self):
        """
        Go offline

        Returns:
            str: 'success'
        """
        if self.token:
            url = self.base + f'api/user/offline'
            response = requests.patch(url, headers=self.headers)
            if response.status_code == HttpStatus.NO_CONTENT:
                return 'success'
            else:
                raise Exception(f'Request Error[{response.status_code}] (offline)')
        else:
            raise Exception('Message: Token is required.')


    ##############  Basic Operations   ##############
    def send_stamp(self, user_id, stamp_id, quantity):
        """
        Send stamp message

        Args:
            user_id: Recipient user ID
            stamp_id: Stamp ID
            quantity: Send quantity

        Returns:
            Response: Response object
        """
        if self.token:
            url = self.base + f'api/stamp_messages'
            data = {
                "message[user_id]": user_id,
                "message[stamp_id]": stamp_id,
                "message[stamp_count]": quantity
            }
            response = requests.post(url, headers=self.headers, data=data)
            if response.status_code == HttpStatus.NO_CONTENT:
                return response
            else:
                raise Exception(f'Request Error[{response.status_code}] (stamp message)')
        else:
            raise Exception('Message: Token is required.')

    def send_message(self, room_id, content):
        """
        Send text message

        Args:
            room_id: Room ID
            content: Message content

        Returns:
            Dict: Sent message information
        """
        if self.token:
            url = self.base + f'api/rooms/{room_id}/messages'
            data = {
                "message[uid]": uuid4(),
                "message[body]": content
            }
            response = requests.post(url, headers=self.headers, data=data)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (send message)')
        else:
            raise Exception('Message: Token is required.')

    def request_friend(self, user_id):
        """
        Send friend request

        Args:
            user_id: User ID

        Returns:
            Dict: Response information
        """
        if self.token:
            url = self.base + f'api/friends'
            data = {
                "user_id": user_id
            }
            response = requests.post(url, headers=self.headers, data=data)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (request friend)')
        else:
            raise Exception('Message: Token is required.')

    def delete_requested(self, user_id):
        """
        Delete sent friend request

        Args:
            user_id: User ID

        Returns:
            Dict: Response information
        """
        if self.token:
            url = self.base + f'api/friendships/{user_id}/retire'
            response = requests.delete(url, headers=self.headers)
            if response.status_code == HttpStatus.OK:
                return response.json()
            else:
                raise Exception(f'Request Error[{response.status_code}] (delete requested)')
        else:
            raise Exception('Message: Token is required.')
