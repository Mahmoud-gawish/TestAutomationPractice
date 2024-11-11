import json
from typing import Dict, Optional


class LocatorLoader:
    def __init__(self, page: str):
        """
        Initialize the LocatorLoader with the specific page's locator JSON file and a single config file for device type.

        :param page: The name of the page (e.g., "login" or "home"), which corresponds to the locator file (e.g., "login_locators.json").
        """
        self.locator_file = f"{page}_locators.json"  # Page-specific locator file
        self.config_file = 'config.json'  # Single config file for device type
        self.locators = self._load_locators()
        self.device_type = self._load_device_type()

    def _load_locators(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Load locators from the page-specific JSON file and return as a dictionary."""
        try:
            with open(self.locator_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Locator file '{self.locator_file}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error parsing JSON in the file '{self.locator_file}'.")

    def _load_device_type(self) -> str:
        """Load device type from the config JSON file."""
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config.get("device_type", "android").lower()  # Default to 'android'
        except FileNotFoundError:
            raise Exception(f"Config file '{self.config_file}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error parsing JSON in the file '{self.config_file}'.")

    def get_locator(self, name: str) -> Optional[Dict[str, str]]:
        """
        Retrieve the locator for the given name based on the configured device type.

        :param name: The name of the locator as defined in the JSON.
        :return: Dictionary containing the locator type and value.
        """
        platform_key = f"{self.device_type}_locator"

        locator_info = self.locators.get(name)
        if not locator_info:
            raise KeyError(f"No locator found for '{name}' in '{self.locator_file}'.")

        platform_locator = locator_info.get(platform_key)
        if not platform_locator:
            raise KeyError(f"No locator found for '{name}' on platform '{self.device_type}'.")

        return platform_locator


# Example usage
if __name__ == "__main__":
    # Initialize for a specific page
    loader = LocatorLoader(page='login')
    locator = loader.get_locator("login_button")
    print(f"Locator for login_button on {loader.device_type}: {locator}")