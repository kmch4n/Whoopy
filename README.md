# Whoopy 👋

## About
Whoopy is a Python library for interacting with the Whoo location-sharing app API.

**Note**: This code is created for educational purposes only and is not intended for bot operations.

## Features

- Token-based and email/password authentication
- Account creation and management
- Friend management (send requests, approve, delete)
- Location updates and retrieval
- Send messages and stamps
- Online/offline status management

## Installation

```bash
pip install -e .
```

Or from requirements.txt:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from whoopy import Client, BatteryState

# Authenticate with token
client = Client(access_token='your_token_here')

# Or authenticate with email and password
client = Client(email='your@email.com', password='your_password')
```

### Account Management

```python
# Get current user information
user_info = client.info()
print(user_info)

# Update account information
client.update_account(
    name="New Name",
    username="new_username",
    profile_image="image_url"
)

# Create a new account
client = Client()  # Initialize without authentication
account = client.create_account(
    email="user@example.com",
    password="password123",
    name="Username",
    profile_image="profile_images/images/default.jpeg",
    username="username123",
    location={"latitude": 35.6762, "longitude": 139.6503}  # Optional
)
```

### Friend Management

```python
# Get friends list
friends = client.get_friends()

# Send friend request
client.request_friend(user_id=12345)

# Get pending requests
requested = client.get_requested()

# Cancel friend request
client.delete_requested(user_id=12345)

# Get specific user information
user = client.get_user(user_id=12345, friends=True)

# Search for user by display name
user = client.find_user("username")
```

### Location Operations

```python
# Update location
location = {"latitude": 35.6762, "longitude": 139.6503}
client.update_location(
    location=location,
    level=80,  # Battery level (0-100)
    state=BatteryState.DISCHARGING,  # Battery state
    speed=5.0,  # Speed (km/h)
    stayed_at="2024-01-01 12:00:00 +0000"  # Optional
)

# Get friends' locations
locations = client.get_locations()
for username, loc in locations.items():
    print(f"{username}: {loc['latitude']}, {loc['longitude']}")
    print(f"Map link: {loc['map']}")

# Request location update
client.reacquire_location(user_id=12345)
```

### Messaging

```python
# Send text message
client.send_message(room_id="room_id", content="Hello!")

# Send stamp
client.send_stamp(user_id=12345, stamp_id=83, quantity=1)
```

### Status Management

```python
# Go online
client.online()

# Go offline
client.offline()
```

## API Reference

### Client Class

#### Initialization

```python
Client(access_token=None, verbose=True, email=None, password=None)
```

**Parameters:**
- `access_token`: Access token (optional)
- `verbose`: Display login success message (default: True)
- `email`: Email address (use with password)
- `password`: Password (use with email)

#### Authentication Methods

- `email_login(email, password)` - Login with email/password
- `create_account(email, password, name, profile_image, username, location=None)` - Create account

#### Account Management Methods

- `info()` - Get current user information
- `update_account(name=None, profile_image=None, username=None)` - Update account information
- `delete_account(alert=True)` - Delete account

#### Friend Management Methods

- `get_friends()` - Get friends list
- `get_requested()` - Get pending friend requests
- `get_user(user_id, friends=False)` - Get user information
- `find_user(user_name)` - Search for user by display name
- `request_friend(user_id)` - Send friend request
- `delete_requested(user_id)` - Cancel friend request

#### Location Methods

- `update_location(location, level=100, state=BatteryState.UNKNOWN, speed=0.0, stayed_at=None, horizontal_accuracy=None)` - Update location
- `get_locations(user_id=None)` - Get friends' locations
- `reacquire_location(user_id)` - Request location update

#### Messaging Methods

- `send_message(room_id, content)` - Send text message
- `send_stamp(user_id, stamp_id, quantity)` - Send stamp

#### Status Methods

- `online()` - Go online
- `offline()` - Go offline

### BatteryState Enum

Enum representing battery states:

- `BatteryState.UNKNOWN` (0) - Unknown
- `BatteryState.CHARGING` (1) - Charging
- `BatteryState.FULL` (2) - Full
- `BatteryState.DISCHARGING` (3) - Discharging

### HttpStatus Enum

Enum representing HTTP status codes:

- `HttpStatus.OK` (200)
- `HttpStatus.NO_CONTENT` (204)
- `HttpStatus.BAD_REQUEST` (400)
- `HttpStatus.UNAUTHORIZED` (401)
- `HttpStatus.FORBIDDEN` (403)
- `HttpStatus.NOT_FOUND` (404)
- `HttpStatus.INTERNAL_SERVER_ERROR` (500)

## Examples

See `examples.py` for detailed sample code.

## License

MIT License
