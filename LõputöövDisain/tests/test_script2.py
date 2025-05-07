import sys
import os
import time
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from db_connection import insert_test_result

sys.stdout.reconfigure(encoding='utf-8')  


url = "https://artdoors.eu/"
test_name = "Artdoors EU Test"


browser_options = {
    "Chrome": webdriver.Chrome,
    "Firefox": webdriver.Firefox,
    "Edge": webdriver.Edge
}


common_args = ["--ignore-certificate-errors"]
chrome_args = common_args + ["--disable-logging", "--log-level=3"]

browser_configs = {
    "Chrome": {"driver": browser_options["Chrome"], "args": chrome_args},
    "Firefox": {"driver": browser_options["Firefox"], "args": common_args},
    "Edge": {"driver": browser_options["Edge"], "args": common_args},
}

def extract_subpages(driver, base_url):
    """Extracts valid subpage URLs from the main page."""
    driver.get(base_url)
    subpages = {
        link.get_attribute("href")
        for link in driver.find_elements(By.TAG_NAME, "a")
        if link.get_attribute("href") and urlparse(link.get_attribute("href")).netloc == urlparse(base_url).netloc
    }
    return list(subpages)

def click_element(driver, element):
    """Attempts to click an element using JavaScript as a fallback."""
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)

def interact_with_forms(driver):
    """Fills and submits forms on a webpage."""
    for form in driver.find_elements(By.TAG_NAME, "form"):
        for field in form.find_elements(By.TAG_NAME, "input") + form.find_elements(By.TAG_NAME, "textarea"):
            try:
                field_type = field.get_attribute("type")
                field.send_keys({
                    "text": "Test Name" if "name" in field.get_attribute("name" or "").lower() else "Sample Text",
                    "email": "test@example.com",
                    "password": "testpassword",
                }.get(field_type, ""))
            except:
                pass
        
        try:
            click_element(driver, form.find_element(By.XPATH, ".//button[@type='submit'] | .//input[@type='submit']"))
        except:
            pass

def run_tests(driver, test_url):
    """Runs all tests on a given page."""
    start_time = time.time()
    status, error_message = "Passed", None
    try:
        driver.get(test_url)
        print(f"\n🔵 Testing: {test_url}")

  
        if test_url.startswith("https://"):
            print("✅ SSL Enabled")
        else:
            status, error_message = "Failed", "SSL missing"
            print("❌ No SSL (HTTPS)")

        
        response = requests.get(test_url)
        for header in ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]:
            print(f"✅ {header} Found" if header in response.headers else f"❌ {header} Missing")
        
        
        if not driver.find_elements(By.TAG_NAME, "nav"):
            status, error_message = "Failed", "Navigation missing"
            print("⚠️ No Navigation Menu")
        else:
            print("✅ Navigation Menu Found")
        
        
        for button in driver.find_elements(By.TAG_NAME, "button"):
            try:
                click_element(driver, button)
                print(f"✅ Clicked: {button.text}")
            except:
                print(f"⚠️ Failed Click: {button.text}")

        
        interact_with_forms(driver)

       
        for link in driver.find_elements(By.TAG_NAME, "a"):
            try:
                if (href := link.get_attribute("href")) and requests.get(href, timeout=5).status_code == 404:
                    print(f"❌ Broken Link: {href}")
            except:
                pass

       
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present()).dismiss()
            print("✅ Popup Closed")
        except:
            pass

        
        if isinstance(driver, webdriver.Chrome):
            try:
                subprocess.run(["lighthouse", test_url, "--quiet", "--chrome-flags=--headless", "--output=json", "--output-path=lighthouse.json"], check=True)
                print("✅ Lighthouse Audit Complete")
            except:
                print("⚠️ Lighthouse Failed")
    
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        status, error_message = "Failed", str(e)
    
    finally:
        execution_time = round(time.time() - start_time, 2)
        insert_test_result(test_name, test_url, status, error_message, execution_time)


for browser_name, config in browser_configs.items():
    print(f"\n🟡 Testing with {browser_name}")
    options = webdriver.ChromeOptions() if browser_name == "Chrome" else webdriver.FirefoxOptions() if browser_name == "Firefox" else webdriver.EdgeOptions()
    for arg in config["args"]:
        options.add_argument(arg)
    
    driver = config["driver"](options=options)
    try:
        for page in extract_subpages(driver, url):
            run_tests(driver, page)
    finally:
        driver.quit()

print("\n✅ All tests completed.")
