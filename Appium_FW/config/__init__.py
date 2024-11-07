# config/__init__.py

# Define constants
TIMEOUT = 30
DEFAULT_PLATFORM = "android"
APPIUM_HOST = "http://localhost:4723"

# Define shared configurations
DEFAULT_CAPS = {
    "platformName": DEFAULT_PLATFORM,
    "automationName": "UiAutomator2",
    "noReset": True
}