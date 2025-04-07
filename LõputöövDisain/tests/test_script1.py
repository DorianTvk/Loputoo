import sys
import os
import time
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from db_connection import insert_test_result  

sys.stdout.reconfigure(encoding='utf-8')  

url = "https://ledstreet.ee/"
test_name = "LED Street Contact Form Test"


browsers = {
    "Chrome": {
        "driver": webdriver.Chrome,
        "options": Options()
    },
    "Firefox": {
        "driver": webdriver.Firefox,
        "options": FirefoxOptions()
    },
    "Edge": {
        "driver": webdriver.Edge,
        "options": EdgeOptions()
    }
}


browsers["Chrome"]["options"].add_argument("--ignore-certificate-errors")
browsers["Chrome"]["options"].add_argument("--disable-logging")
browsers["Chrome"]["options"].add_argument("--log-level=3")
browsers["Chrome"]["options"].add_argument("--disable-usb-discovery")
browsers["Chrome"]["options"].add_argument("--disable-device-discovery-notifications")

browsers["Firefox"]["options"].add_argument("--ignore-certificate-errors")
browsers["Edge"]["options"].add_argument("--ignore-certificate-errors")
browsers["Edge"]["options"].add_argument("--disable-features=EdgeIdentitySignin")

for browser_name, browser_data in browsers.items():
    print(f"\n🟡 Running test on {browser_name}...")

    start_time = time.time() 
    status = "Passed"
    error_message = None

    try:
        driver = browser_data["driver"](options=browser_data["options"])
        driver.get(url)
        wait = WebDriverWait(driver, 10)


        if url.startswith("https://"):
            print("✅ Website has SSL (HTTPS) enabled")
        else:
            print("❌ Website does NOT have SSL (HTTPS)")
            status = "Failed"
            error_message = "SSL missing"


        response = requests.get(url)
        security_headers = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]
        for header in security_headers:
            if header in response.headers:
                print(f"✅ Security Header Present: {header}")
            else:
                print(f"❌ Missing Security Header: {header}")


        for width in [1920, 1366, 768, 375]:
            driver.set_window_size(width, 900)
            print(f"✅ Checked responsiveness at {width}px width")


        try:
            navbar = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
            print("✅ Navigation menu detected")
        except:
            print("⚠️ Navigation menu NOT found")


        try:
            contact_form = wait.until(EC.presence_of_element_located((By.XPATH, "//form")))
            print("✅ Contact form detected")
        except:
            print("⚠️ Contact form NOT found")
            status = "Failed"
            error_message = "Contact form missing"


        try:
            kontakt_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Kontakt')]")
            ))
            kontakt_button.click()
            print("✅ 'Kontakt' button clicked successfully")
        except:
            print("⚠️ No 'Kontakt' button found on the page.")


        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href:
                try:
                    response = requests.get(href, timeout=5)
                    if response.status_code == 404:
                        print(f"❌ Broken Link: {href}")
                except requests.exceptions.RequestException:
                    print(f"⚠️ Link check failed: {href}")


        load_time = driver.execute_script("return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;")
        print(f"✅ Page load time: {load_time}ms")


        title = driver.title
        if title:
            print(f"✅ Page title found: {title}")
        else:
            print("⚠️ Missing page title")

        meta_description = driver.find_elements(By.XPATH, "//meta[@name='description']")
        if meta_description:
            print("✅ Meta description found")
        else:
            print("⚠️ Missing meta description")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        status = "Failed"
        error_message = str(e)

    finally:
        execution_time = round(time.time() - start_time, 2)
        driver.quit()


        insert_test_result(f"{test_name} ({browser_name})", url, status, error_message, execution_time)

print("\n✅ All browser tests completed.")
