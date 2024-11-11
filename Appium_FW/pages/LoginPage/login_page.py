from Appium_FW.Utils.LocatorLoader import LocatorLoader
from Appium_FW.Utils.AppiumActions import AppiumActions


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.locator_loader = LocatorLoader(page='login') # Initialize LocatorLoader
        self.actions = AppiumActions(driver, self.locator_loader)  # Initialize AppiumActions with LocatorLoader

    def login(self, username: str, password: str):
        """Performs the login action using provided username and password."""

        # Enter username
        self.actions.input_text("username_field", username)

        # Enter password
        self.actions.input_text("password_field", password)

        # Click login button
        self.actions.click("login_button")