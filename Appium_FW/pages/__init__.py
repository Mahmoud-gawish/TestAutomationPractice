# __init__.py in Appium_FW/Pages

# Import specific pages to make them accessible from the Pages package
from .LoginPage import login_page

# List all classes available for import when using "from Pages import *"
__all__ = ["login_page.py"]