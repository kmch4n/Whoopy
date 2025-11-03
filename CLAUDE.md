# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Whoopy is a Python library for interacting with the Whoo location-sharing app API. This is an educational project wrapping the Whoo REST API (https://www.wh00.ooo/).

**Important**: This library is for educational purposes only and is not intended for bot operations.

## Development Setup

```bash
# Install in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt
```

## Architecture

### Core Design

The library uses a **single unified Client class** (`whoopy/client.py`) that provides all API functionality. This is the primary interface users interact with.

**Key architectural points:**

1. **Client Class** (`whoopy/client.py`): All-in-one API client
   - Handles authentication (token-based or email/password)
   - Contains all API methods organized by function (account, friends, location, messaging, status)
   - Automatically validates token on initialization
   - Sets `self.token = True/None` to track authentication state

2. **Legacy Files**: The following files exist but are **NOT used** by the main Client:
   - `whoopy/location.py` - Legacy location handler
   - `whoopy/user.py` - Legacy user handler
   - `whoopy/profile.py` - Legacy profile handler
   - `whoopy/utils.py` - Legacy utilities

   These should not be modified or referenced when working with the Client class.

3. **Enums** (`whoopy/enums.py`): Type-safe constants
   - `BatteryState`: UNKNOWN(0), CHARGING(1), FULL(2), DISCHARGING(3)
   - `HttpStatus`: Standard HTTP codes
   - Constants: `SPEED_CONVERSION_FACTOR`, `DEFAULT_BATTERY_LEVEL`, `DEFAULT_BATTERY_STATE`

4. **Package Exports** (`whoopy/__init__.py`): Only exports Client, BatteryState, HttpStatus

### Authentication Flow

```python
# Three initialization modes:
cl = Client(access_token='...')              # Token auth
cl = Client(email='...', password='...')     # Email/password (calls email_login internally)
cl = Client()                                 # Unauthenticated (for create_account)
```

On init with token/email:
1. Sets Authorization header
2. Calls `GET /api/my` to validate
3. Sets `self.token = True` on success or raises Exception

### API Method Organization

Methods in `Client` are grouped by function (see comments in code):

- **Account Settings**: `email_login`, `create_account`, `update_account`, `delete_account`
- **Background Processing**: `info`, `get_requested`, `get_friends`, `get_user`, `find_user`, `reacquire_location`, `update_location`, `get_locations`, `online`, `offline`
- **Basic Operations**: `send_stamp`, `send_message`, `request_friend`, `delete_requested`

### API Endpoint Patterns

Base URL: `https://www.wh00.ooo/`

Key patterns:
- All authenticated methods check `if self.token` or `if not self.token` before making requests
- Location data uses nested dict: `user_location[latitude]`, `user_battery[level]`
- Speed is converted: km/h → m/s using `SPEED_CONVERSION_FACTOR`
- Battery level is sent as decimal: `level / 100`
- The `get_user()` method handles pagination automatically when `friends=True`

## Coding Conventions

### Variable Naming
- **Always use `cl`** for Client instances in examples and documentation (not `client`)
- This convention is enforced across README.md, examples.py, and all documentation

### Commit Message Format
Use the format: `[emoji] Description`

Examples:
- `[✨] Add new feature`
- `[🐛] Fix bug`
- `[📚] Update documentation`
- `[♻️] Refactor code`

### Documentation Standards
- All documentation and code comments must be in **English**
- Docstrings use Google style format
- Include parameter types and return types in docstrings

### Error Handling
- Use `HttpStatus` enum for status code comparisons
- Raise Exception with format: `f'Request Error[{status_code}] (operation_name)'`
- Check token requirement: `if not self.token: raise Exception('Message: Token is required.')`

## Testing

Currently no automated tests. To test manually:

```python
from whoopy import Client, BatteryState

# Test with your token
cl = Client(access_token='your_token')
print(cl.info())
```

See `examples.py` for comprehensive usage examples.

## Package Structure

```
whoopy/
├── __init__.py          # Exports: Client, BatteryState, HttpStatus
├── client.py            # Main Client class (ALL functionality here)
├── enums.py             # BatteryState, HttpStatus, constants
├── location.py          # Legacy (not used by Client)
├── user.py              # Legacy (not used by Client)
├── profile.py           # Legacy (not used by Client)
└── utils.py             # Legacy (not used by Client)
```

## Key API Methods

### Authentication
- `email_login(email, password)` → Returns dict with `access_token`
- `create_account(email, password, name, profile_image, username, location=None)` → Can optionally set initial location

### Location Updates
- `update_location(location, level, state, speed, stayed_at, horizontal_accuracy)`
  - `location`: Dict with `latitude`, `longitude`
  - `state`: BatteryState enum value
  - Returns location data

### Pagination Example
The `get_user(user_id, friends=True)` method demonstrates pagination handling:
- Checks `js["next_page"]` for page count
- Loops through pages calling `/api/v2/users/{user_id}/friends?page={i+1}`
- Aggregates results into `js["friends"]` array

## Common Gotchas

1. **Speed conversion**: API expects m/s, but library accepts km/h (automatically converts)
2. **Battery level**: API expects 0-1 decimal, library accepts 0-100 percentage (automatically converts)
3. **Token validation**: Client automatically validates token on init, will raise Exception if invalid
4. **Legacy files**: Don't confuse `whoopy/location.py` etc. with the Client methods - they're separate codebases

## Additional Formatting Instruction

- After generating the final commit message or code content:
- Perform full formatting of the entire output.
- Indentation must be exactly 4 spaces.
- If applying this formatting would reduce readability or alter layout meaning, explicitly notify the user and skip formatting for that section only.
- Do not modify content semantics when formatting.


## 📝 Instruction
After completing **all fixes or updates**, propose a **final commit message** in English using the [Gitmoji](https://gitmoji.dev/) convention.

### Requirements
1. Follow this exact format:
2. Use **concise, descriptive wording** that summarizes what has been improved, fixed, or updated.
3. Consider the **entire set of commits** shown (not just the latest one).
4. Provide **only the final commit message** — no explanations or bullet points.
5. The message should feel natural as a single, polished Git commit summary.


## 🧩 Example Commit History (OCR Extracted)

Below is an example commit history (extracted from an image):

- [🐛] Fix arrow key navigation issue in menu bar  
- [💄] Fix layout issues on large screens  
- [♻️] Reorder HTML sections and fix incorrect footer link  
- [✨] Add favicon and OGP tags for browser display and LINE preview  
- [🧩] Update header menu text layout and fix line-breaking issue  
- [🎨] Minor fixes in footer style  
- [🔧] Adjust index.html based on updated README.md  
- [🧾] Minor fixes in README.md  
- [💄] Improve README.md readability and fix line break issues  
- [📝] Revise README.md with major content updates  


## 💬 Example Output
Based on the commit history above, a well-formed final commit message might look like:

## 💡 Notes
- Choose **appropriate emojis** according to the change type:  
  - [🐛] Bug fix  
  - [💄] UI or layout improvement  
  - [♻️] Code refactor  
  - [✨] New feature or enhancement  
  - [📝] Documentation change  
  - [🚀] Performance or deployment improvement  
- Ensure your summary reflects **the full scope of work completed**, not individual steps.
- Keep it **professional, concise, and human-readable** — just like a real Git commit message.

**Use this prompt to automatically generate a clean, Gitmoji-compliant commit message after all fixes are completed.**