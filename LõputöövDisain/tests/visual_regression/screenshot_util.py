import os
from datetime import datetime
from selenium.webdriver.common.by import By

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(url_path):
    return url_path.strip('/').replace('/', '_') or 'homepage'

def take_screenshot(driver, domain_folder, url_path):
    ensure_dir(domain_folder)
    page_name = sanitize_filename(url_path)
    file_path = os.path.join(domain_folder, f"{page_name}.png")
    driver.save_screenshot(file_path)
    return file_path

def save_screenshot(driver, url, test_name, is_baseline=False):
    domain = url.split("//")[-1].strip("/")
    folder = os.path.join("screenshots", domain, "baseline" if is_baseline else "new")
    if not os.path.exists(folder):
        os.makedirs(folder)
    return take_screenshot(driver, folder, test_name)

def update_baseline(domain_folder, url_path, driver):
    """
    Saves a screenshot as the new baseline, overwriting the previous one.
    """
    return take_screenshot(driver, domain_folder, url_path)
