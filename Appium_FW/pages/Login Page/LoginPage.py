from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Appium_FW.utils.LocatorLoader import LocatorLoader


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.locator_loader = LocatorLoader()

    def get_element(self, locator_name):
        """Helper method to locate an element."""
        locator = self.locator_loader.get_locator(locator_name)
        locator_type = locator['type']
        locator_value = locator['value']
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((getattr(AppiumBy, locator_type.upper()), locator_value))
        )

    def login(self, username, password):
        """Example method to perform login."""
        username_field = self.get_element("username_field")
        username_field.send_keys(username)

        password_field = self.get_element("password_field")
        password_field.send_keys(password)

        login_button = self.get_element("login_button")
        login_button.click()