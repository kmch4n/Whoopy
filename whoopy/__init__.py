"""
Whoopy - A Python library for interacting with the Whoo location-sharing app

This library is a Python wrapper for the Whoo API.
"""

from .client import Whoopy
from .enums import BatteryState, HttpStatus

__version__ = "1.0.0"
__all__ = ["Whoopy", "BatteryState", "HttpStatus"]
