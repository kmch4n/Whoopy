"""
Whoopy API Usage Examples
"""
from whoopy import Client, BatteryState


def example_authentication():
    """Authentication examples"""
    print("=== Authentication Examples ===")

    # Method 1: Initialize with access token
    cl = Client(access_token='your_token_here')

    # Method 2: Initialize with email and password
    cl = Client(email='your@email.com', password='your_password')

    # Method 3: Initialize without authentication (for create_account, etc.)
    cl = Client()

    print("Authentication complete")


def example_account_management(cl):
    """Account management examples"""
    print("\n=== Account Management Examples ===")

    # Get current user information
    info = cl.info()
    print(f"User info: {info}")

    # Update account information
    cl.update_account(
        name="New Name",
        username="new_username"
    )
    print("Account information updated")

    # Delete account (with confirmation)
    # result = cl.delete_account(alert=True)


def example_friend_management(cl):
    """Friend management examples"""
    print("\n=== Friend Management Examples ===")

    # Get friends list
    friends = cl.get_friends()
    print(f"Number of friends: {len(friends.get('friends', []))}")

    # Send friend request
    user_id = 12345
    result = cl.request_friend(user_id)
    print(f"Friend request sent: {result}")

    # Get pending requests
    requested = cl.get_requested()
    print(f"Pending requests: {requested}")

    # Cancel request
    # cl.delete_requested(user_id)

    # Get specific user information (with friends list)
    user_info = cl.get_user(user_id, friends=True)
    print(f"User info: {user_info.get('display_name')}")

    # Search for user by display name
    user = cl.find_user("username")
    print(f"Found user: {user}")


def example_location_operations(cl):
    """Location operation examples"""
    print("\n=== Location Operation Examples ===")

    # Update location
    location = {
        "latitude": 35.6762,  # Tokyo
        "longitude": 139.6503
    }

    result = cl.update_location(
        location=location,
        level=85,  # Battery level 85%
        state=BatteryState.DISCHARGING,
        speed=5.0,  # 5 km/h
        stayed_at="2024-01-01 12:00:00 +0000"
    )
    print(f"Location updated: {result}")

    # Get friends' locations
    locations = cl.get_locations()
    for username, loc in locations.items():
        print(f"{username}: {loc['latitude']}, {loc['longitude']}")
        print(f"  Map: {loc['map']}")

    # Request location from specific friend
    cl.reacquire_location(user_id=12345)


def example_messaging(cl):
    """Messaging feature examples"""
    print("\n=== Messaging Feature Examples ===")

    # Send text message
    room_id = "room_id_here"
    message = cl.send_message(room_id, "Hello!")
    print(f"Message sent: {message}")

    # Send stamp
    user_id = 12345
    stamp_id = 83
    cl.send_stamp(user_id, stamp_id, quantity=1)
    print("Stamp sent")


def example_status_management(cl):
    """Status management examples"""
    print("\n=== Status Management Examples ===")

    # Go online
    cl.online()
    print("Now online")

    # Go offline
    # cl.offline()
    # print("Now offline")


def example_account_creation():
    """Account creation examples"""
    print("\n=== Account Creation Examples ===")

    cl = Client()  # No authentication

    # Basic account creation
    account = cl.create_account(
        email="new_user@example.com",
        password="SecurePassword123",
        name="New User",
        profile_image="profile_images/images/default.jpeg",
        username="new_user_123"
    )
    print(f"Account created: {account}")

    # Create account with location
    location = {"latitude": 35.6762, "longitude": 139.6503}
    account_with_location = cl.create_account(
        email="another_user@example.com",
        password="SecurePassword456",
        name="Location User",
        profile_image="profile_images/images/default.jpeg",
        username="location_user",
        location=location
    )
    print(f"Account with location created: {account_with_location}")


def main():
    """Main function - Run all examples"""
    # Authentication examples
    # example_authentication()

    # Valid token required for actual operations
    try:
        cl = Client(access_token='your_valid_token_here')

        # Run examples for each feature
        example_account_management(cl)
        example_friend_management(cl)
        example_location_operations(cl)
        example_messaging(cl)
        example_status_management(cl)

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Please set a valid access token")

    # Account creation examples
    # example_account_creation()


if __name__ == "__main__":
    main()
