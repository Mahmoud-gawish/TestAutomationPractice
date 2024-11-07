from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging


class AppiumActions:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)  # Set default wait time here

    def find_element(self, locator_type: str, locator_value: str, timeout: int = 10):
        """
        Find an element with explicit wait.

        Parameters:
            locator_type (str): Locator type (e.g., 'ID', 'XPATH').
            locator_value (str): The actual locator value.
            timeout (int): Custom timeout for waiting (default: 10 seconds).

        Returns:
            WebElement: The found element.

        Raises:
            TimeoutException: If the element is not found within the specified time.
        """
        try:
            # Convert string locator_type to AppiumBy attribute
            locator_strategy = getattr(AppiumBy, locator_type.upper(), None)
            if not locator_strategy:
                raise ValueError(f"Invalid locator type: {locator_type}")

            # Wait until element is present
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_strategy, locator_value))
            )
            return element
        except TimeoutException:
            logging.error(f"Timeout: Element not found with {locator_type}: {locator_value}")
            raise TimeoutException(f"Element not found with {locator_type}: {locator_value}")
        except Exception as e:
            logging.error(f"Error finding element with {locator_type}: {locator_value} - {str(e)}")
            raise

    def click(self, locator_type: str, locator_value: str, timeout: int = 10):
        """Click on an element with explicit wait and error handling."""
        try:
            element = self.find_element(locator_type, locator_value, timeout)
            element.click()
            logging.info(f"Clicked on element with {locator_type}: {locator_value}")
        except Exception as e:
            logging.error(f"Error clicking element with {locator_type}: {locator_value} - {str(e)}")
            raise

    def input_text(self, locator_type: str, locator_value: str, text: str, timeout: int = 10):
        """Input text into an element with explicit wait and error handling."""
        try:
            element = self.find_element(locator_type, locator_value, timeout)
            element.clear()  # Clear existing text
            element.send_keys(text)
            logging.info(f"Entered text '{text}' into element with {locator_type}: {locator_value}")
        except Exception as e:
            logging.error(f"Error entering text in element with {locator_type}: {locator_value} - {str(e)}")
            raise

    def get_text(self, locator_type: str, locator_value: str, timeout: int = 10) -> str:
        """Retrieve text from an element with explicit wait and error handling."""
        try:
            element = self.find_element(locator_type, locator_value, timeout)
            element_text = element.text
            logging.info(f"Retrieved text '{element_text}' from element with {locator_type}: {locator_value}")
            return element_text
        except Exception as e:
            logging.error(f"Error retrieving text from element with {locator_type}: {locator_value} - {str(e)}")
            raise

    def scroll_to_element(self, locator_type: str, locator_value: str, max_swipes: int = 5):
        """Scrolls to the element, performing swipe actions until it's found or max_swipes is reached."""
        for _ in range(max_swipes):
            try:
                element = self.find_element(locator_type, locator_value, timeout=3)
                return element
            except TimeoutException:
                self.swipe('down')
        raise TimeoutException(f"Element not found with {locator_type}: {locator_value} after {max_swipes} swipes.")

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
        """Switches to a specific context (e.g., WEBVIEW or NATIVE_APP)"""
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