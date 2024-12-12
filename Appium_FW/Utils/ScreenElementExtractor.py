from appium import webdriver
import xml.etree.ElementTree as ET
import json
import os
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from appium.options.android import UiAutomator2Options


class ScreenElementExtractor:
    def __init__(self, driver: webdriver.Remote, output_file: str = "elements.json",
                 page_source_file: str = "page_source.xml"):
        """
        Initialize the extractor.

        :param driver: Appium WebDriver instance.
        :param output_file: Path to the output JSON file.
        :param page_source_file: Path to save the page source XML file.
        """
        self.driver = driver
        self.output_file = output_file
        self.page_source_file = page_source_file
        self.elements = {}

    def save_page_source(self):
        """Fetch and save the current page source to an XML file."""
        page_source = self.driver.page_source
        with open(self.page_source_file, "w", encoding="utf-8") as file:
            file.write(page_source)

    def parse_screen_source(self):
        """Parse the saved page source XML and extract elements."""
        if not os.path.exists(self.page_source_file):
            raise FileNotFoundError(
                f"The file {self.page_source_file} does not exist. Please fetch the page source first.")

        try:
            tree = ET.parse(self.page_source_file)
            root = tree.getroot()
            self._extract_elements(root)
        except ET.ParseError as e:
            print(f"Error parsing screen source: {e}")

    def _extract_elements(self, node):
        """Recursive method to extract element locators."""
        # Determine the element name
        element_name = (
                node.attrib.get("text", "").strip()
                or node.attrib.get("content-desc", "").strip()
                or node.attrib.get("resource-id", "").strip()
                or f"Unnamed_{node.tag}"
        )

        # Determine the locator strategy
        if "resource-id" in node.attrib and node.attrib["resource-id"].strip():
            locator = f"//*[@resource-id='{node.attrib['resource-id'].strip()}']"
        elif "text" in node.attrib and node.attrib["text"].strip():
            locator = f"//*[contains(@text,'{node.attrib['text'].strip()}')]"
        elif "content-desc" in node.attrib and node.attrib["content-desc"].strip():
            locator = f"//*[@content-desc='{node.attrib['content-desc'].strip()}']"
        elif "class" in node.attrib and node.attrib["class"].strip():
            locator = f"//*[contains(@class,'{node.attrib['class'].strip()}')]"
        else:
            locator = None

        # Add the element to the JSON structure
        if locator:
            self.elements[element_name] = {"xpath": locator}

        # Recursively process child elements
        for child in list(node):
            self._extract_elements(child)

    def save_to_json(self):
        """Save the extracted elements to a JSON file."""
        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump(self.elements, file, indent=4, ensure_ascii=False)

    def extract(self):
        """Main method to fetch the page source, parse it, and save results."""
        self.save_page_source()
        self.parse_screen_source()
        self.save_to_json()


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
        # Initialize the extractor and generate elements
        extractor = ScreenElementExtractor(driver, output_file="elements.json", page_source_file="page_source.xml")
        extractor.extract()
        print(f"Elements saved to {extractor.output_file}")
    finally:
        # Quit the Appium session
        driver.quit()