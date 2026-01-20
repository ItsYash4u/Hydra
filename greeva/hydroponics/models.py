
"""
Hydroponics Models - Using Custom Database Schema
Imports the three custom tables: UserDevice, Device, SensorValue
"""

# Import custom models
from .models_custom import UserDevice, Device, SensorValue

# Export for use in other modules
__all__ = ['UserDevice', 'Device', 'SensorValue']