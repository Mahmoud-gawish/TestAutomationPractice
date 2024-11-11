from selenium.common.exceptions import TimeoutException
import logging
from Appium_FW.Utils.LocatorLoader import LocatorLoader
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AppiumActions:
    def __init__(self, driver, locator_loader: LocatorLoader):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)  # Default wait time
        self.locator_loader = locator_loader  # LocatorLoader instance

    def find_element(self, locator_name: str, timeout: int = 10):
        locator = self.locator_loader.get_locator(locator_name)
        locator_type = getattr(AppiumBy, locator['type'].upper(), None)
        locator_value = locator['value']
        if not locator_type:
            raise ValueError(f"Invalid locator type: {locator['type']}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((locator_type, locator_value))
        )

    def click(self, locator_name: str, timeout: int = 10):
        element = self.find_element(locator_name, timeout)
        element.click()
        logging.info(f"Clicked on element '{locator_name}'")

    def input_text(self, locator_name: str, text: str, timeout: int = 10):
        element = self.find_element(locator_name, timeout)
        element.clear()
        element.send_keys(text)
        logging.info(f"Entered text '{text}' into element '{locator_name}'")

    def get_text(self, locator_name: str, timeout: int = 10) -> str:
        element = self.find_element(locator_name, timeout)
        return element.text

    def scroll_to_element(self, locator_name: str, max_swipes: int = 5):
        """
        Scrolls to an element by locator name, performing swipe actions until it’s found
        or max_swipes is reached.
        """
        locator = self.locator_loader.get_locator(locator_name)
        locator_type = getattr(AppiumBy, locator['type'].upper(), None)
        locator_value = locator['value']

        for _ in range(max_swipes):
            try:
                element = self.find_element(locator_name, timeout=3)
                return element
            except TimeoutException:
                self.swipe('down')
        raise TimeoutException(f"Element '{locator_name}' not found after {max_swipes} swipes.")

    def swipe(self, direction: str = 'up', distance: float = 0.5, duration: int = 1000):
        """Swipe in a specified direction by a certain distance and duration."""
        size = self.driver.get_window_size()
        x, y = size['width'] // 2, size['height'] // 2
        if direction.lower() == 'up':
            self.driver.swipe(x, int(y * (1 + distance)), x, int(y * (1 - distance)), duration)
        elif direction.lower() == 'down':
            self.driver.swipe(x, int(y * (1 - distance)), x, int(y * (1 + distance)), duration)
        elif direction.lower() == 'left':
            self.driver.swipe(int(x * (1 + distance)), y, int(x * (1 - distance)), y, duration)
        elif direction.lower() == 'right':
            self.driver.swipe(int(x * (1 - distance)), y, int(x * (1 + distance)), y, duration)

    def switch_to_context(self, context_name: str):
        """Switches to a specific context (e.g., WEBVIEW or NATIVE_APP)."""
        available_contexts = self.driver.contexts
        if context_name in available_contexts:
            self.driver.switch_to.context(context_name)
            logging.info(f"Switched to context: {context_name}")
        else:
            raise ValueError(f"Context {context_name} not found. Available contexts: {available_contexts}")

    def capture_screenshot(self, file_path: str):
        """Captures a screenshot and saves it to the specified file path."""
        self.driver.save_screenshot(file_path)
        logging.info(f"Screenshot saved to {file_path}")