import json
from appium import webdriver
from appium.options.common import AppiumOptions
from typing import Optional, Dict

class DriverManager:
    _driver: Optional[webdriver.Remote] = None
    _config: Dict = {}

    @classmethod
    def load_config(cls, config_file: str = 'config.json'):
        """Load configuration from JSON file once and store it in the class variable."""
        if not cls._config:  # Load config only if it's not already loaded
            try:
                with open(config_file, 'r') as file:
                    cls._config = json.load(file)
            except FileNotFoundError:
                raise Exception(f"Config file '{config_file}' not found.")
            except json.JSONDecodeError:
                raise Exception(f"Error parsing JSON in the config file '{config_file}'.")

    @classmethod
    def init_driver(cls, app_path: Optional[str] = None) -> webdriver.Remote:
        """Initialize Appium driver with capabilities based on config file."""
        if not cls._config:
            cls.load_config()  # Ensure config is loaded

        options = AppiumOptions()
        device_type = cls._config.get("device_type", "android").lower()  # Default to "android"
        platform_config = cls._config.get(device_type, {})

        for key, value in platform_config.items():
            options.set_capability(key, value)

        if app_path:
            options.set_capability('app', app_path)

        cls._driver = webdriver.Remote('http://localhost:4723', options=options)
        return cls._driver

    @classmethod
    def get_driver(cls) -> webdriver.Remote:
        """Get the current driver instance."""
        if not cls._driver:
            raise Exception("Driver not initialized. Call init_driver() first.")
        return cls._driver

    @classmethod
    def quit_driver(cls):
        """Quit the driver instance."""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None