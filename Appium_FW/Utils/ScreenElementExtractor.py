import xml.etree.ElementTree as ET
import json
import os


class ScreenElementExtractor:
    def __init__(self, screen_source: str = None, xml_file: str = None, output_file: str = "elements.json"):
        """
        Initialize the extractor.

        :param screen_source: XML source as a string.
        :param xml_file: Path to an XML file containing the screen source.
        :param output_file: Path to the output JSON file.
        """
        self.screen_source = screen_source
        self.xml_file = xml_file
        self.output_file = output_file
        self.elements = {}

        if not self.screen_source and not self.xml_file:
            raise ValueError("Either 'screen_source' or 'xml_file' must be provided.")
        if self.xml_file and not os.path.exists(self.xml_file):
            raise FileNotFoundError(f"The file {self.xml_file} does not exist.")

    def _load_screen_source_from_file(self):
        """Load the screen source XML from a file."""
        with open(self.xml_file, "r", encoding="utf-8") as file:
            self.screen_source = file.read()

    def parse_screen_source(self):
        """Parse the screen source XML and extract elements."""
        if self.xml_file and not self.screen_source:
            self._load_screen_source_from_file()

        try:
            tree = ET.ElementTree(ET.fromstring(self.screen_source))
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
        """Main method to parse the source and save results."""
        self.parse_screen_source()
        self.save_to_json()


# Example Usage
if __name__ == "__main__":
    # Option 1: Provide XML as a string
    # screen_source = """
    # <hierarchy>
    #     <node text="Submit" resource-id="com.example:id/button1" content-desc="SubmitButton" class="android.widget.Button" />
    #     <node class="android.widget.TextView" />
    #     <node text="Enter your name" resource-id="com.example:id/inputField" class="android.widget.EditText" />
    # </hierarchy>
    # """
    # extractor = ScreenElementExtractor(screen_source=screen_source, output_file="output.json")
    # extractor.extract()
    # print(f"Elements saved to {extractor.output_file}")

    # Option 2: Provide an XML file path
    # Make sure 'screen_source.xml' exists in the same directory
    xml_file_path = "/Users/mahmoudgawish/PycharmProjects/TestAutomationPractice/Appium_FW/Utils/screen_source.xml"
    extractor = ScreenElementExtractor(xml_file=xml_file_path, output_file="output_from_file.json")
    extractor.extract()
    print(f"Elements saved to {extractor.output_file}")