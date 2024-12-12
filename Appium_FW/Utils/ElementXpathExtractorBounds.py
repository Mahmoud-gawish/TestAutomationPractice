from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import json
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from appium.options.android import UiAutomator2Options

class ElementXpathExtractor:
    def __init__(self, driver, output_file="elements_xpaths.json"):
        """
        Initialize the XPath extractor class.

        :param driver: Appium WebDriver instance.
        :param output_file: Path to save the generated XPaths as a JSON file.
        """
        self.driver = driver
        self.output_file = output_file
        self.elements = []
        self.seen_bounds = set()  # To avoid duplicate bounds

    def get_element_bounds(self, element):
        """
        Retrieve the bounds of the element.

        :param element: Web element to retrieve bounds for.
        :return: Bounds in the format '[x1,y1][x2,y2]' or None if no bounds are found.
        """
        try:
            # Get the bounds attribute of the element
            bounds = element.get_attribute("bounds")
            return bounds  # Bounds will be in the format '[x1,y1][x2,y2]'
        except Exception as e:
            print(f"Error while getting bounds: {e}")
            return None

    def get_element_name(self, element):
        """
        Retrieve the element's name, which could be its text or other identifying attributes.

        :param element: Web element to retrieve the name for.
        :return: The element's name as a string.
        """
        # Priority: text -> resource-id -> class_name
        text = element.get_attribute("text")
        if text:
            return text.strip()

        resource_id = element.get_attribute("resourceId")
        if resource_id:
            return resource_id.strip()

        return element.get_attribute("className")  # Fallback to class name if no text or resource-id

    def generate_xpath(self, class_name, bounds):
        """
        Generate the XPath based on class name and bounds.

        :param class_name: The class name of the element.
        :param bounds: The bounds of the element in the format '[x1,y1][x2,y2]'.
        :return: The generated XPath.
        """
        return f"//{class_name}[@bounds='{bounds}']"

    def extract_elements_xpaths(self):
        """
        Extract elements' XPaths from the current page based on bounds and class name.

        :return: A list of elements with their XPaths.
        """
        # Find all elements on the screen (you can filter based on visibility or other criteria if needed)
        elements = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector()")

        for element in elements:
            class_name = element.get_attribute("className")
            bounds = self.get_element_bounds(element)

            if bounds and bounds not in self.seen_bounds:
                # Ensure we don't process duplicate bounds
                self.seen_bounds.add(bounds)

                # Get the element's name for identification
                element_name = self.get_element_name(element)

                xpath = self.generate_xpath(class_name, bounds)
                self.elements.append({
                    "element_name": element_name,
                    "class_name": class_name,
                    "bounds": bounds,
                    "xpath": xpath
                })

        return self.elements

    def save_to_json(self):
        """
        Save the extracted XPaths to a JSON file.
        """
        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump(self.elements, file, indent=4)

    def extract_and_save(self):
        """
        Extract the elements' XPaths and save to the JSON file.
        """
        self.extract_elements_xpaths()
        self.save_to_json()
        print(f"XPaths saved to {self.output_file}")


# Example Usage
if __name__ == "__main__":
    # Appium Driver Setup (Modify capabilities as needed)
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("automationName", "UIAutomator2")
    options.set_capability("appPackage", "com.swaglabsmobileapp")
    options.set_capability("appActivity", "com.swaglabsmobileapp.MainActivity")
    options.set_capability("udid", "RFCX11506GH")
    options.set_capability("noReset", True)

    # Initialize the driver with Appium's WebDriver
    driver = AppiumWebDriver("http://127.0.0.1:4723", options=options)

    try:
        # Initialize the extractor and extract XPaths
        extractor = ElementXpathExtractor(driver, output_file="elements_xpaths_bounds.json")
        extractor.extract_and_save()
    finally:
        # Quit the Appium session
        driver.quit()