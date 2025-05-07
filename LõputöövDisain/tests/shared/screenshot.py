import os
import logging

from datetime import datetime
from selenium.webdriver.common.by import By

# --- Screenshot on Failure ---
def take_screenshot(driver, test_name):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(file_path)
    logging.info(f"📸 Screenshot saved: {file_path}")
    return file_path