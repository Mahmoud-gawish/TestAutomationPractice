import json
from typing import Dict, Any


class TestDataLoader:
    def __init__(self, data_file: str = 'test_data.json'):
        self.data_file = data_file
        self.test_data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Load test data from the JSON file."""
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Test data file '{self.data_file}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error parsing JSON in the file '{self.data_file}'.")

    def get_test_data(self, test_name: str) -> Dict[str, str]:
        """Retrieve test data for the given test name."""
        if test_name in self.test_data:
            return self.test_data[test_name]
        else:
            raise KeyError(f"No test data found for test '{test_name}' in '{self.data_file}'.")


# Usage example
if __name__ == "__main__":
    loader = TestDataLoader('test_data.json')

    # Replace 'test_login_valid_user' with the actual test name as needed
    test_data = loader.get_test_data('test_login_valid_user')
    print(f"Username: {test_data['username']}, Password: {test_data['password']}")