import unittest
from Appium_FW.pages import login_page # Import the LoginPage class
from Appium_FW.Utils.TestDataLoader import TestDataLoader  # Import the TestDataLoader class
from Appium_FW.Utils.DriverManager import DriverManager  # Import the DriverManager for driver initialization
from Appium_FW.pages.LoginPage.login_page import LoginPage


class LoginTest:

    def setUp(self):
        # Initialize the Appium driver
        self.driver = DriverManager.init_driver()

        # Load the test data from the JSON file
        self.test_data_loader = TestDataLoader('test_data.json')

        # Create an instance of LoginPage with the driver
        self.login_obj = LoginPage(self.driver)

    def test_login_valid_user(self):
        """Test login with valid username and password."""
        test_data = self.test_data_loader.get_test_data('test_login_valid_user')
        username = test_data['username']
        password = test_data['password']

        # Use the LoginPage instance to perform login
        self.login_obj.login(username, password)

        # Verify the login success (you might need to add an actual check, e.g., check for a specific element)

    def test_login_invalid_user(self):
        """Test login with invalid username and password."""
        test_data = self.test_data_loader.get_test_data('test_login_invalid_user')
        username = test_data['username']
        password = test_data['password']

        # Use the LoginPage instance to perform login
        self.login_obj.login(username, password)

        # Verify the login failure (you might need to add an actual check for login failure)

    @staticmethod
    def tearDown():
        # Close the driver after tests
        DriverManager.quit_driver()


if __name__ == "__main__":
    unittest.main()