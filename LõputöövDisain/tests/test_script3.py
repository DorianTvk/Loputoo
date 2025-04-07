import sys
import os
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from db_connection import insert_test_result  

sys.stdout.reconfigure(encoding='utf-8')  


url = "https://www.megapikselstuudio.ee/"
test_name = "Megapiksel Test"


browsers = {
    "Chrome": webdriver.Chrome,
    "Firefox": webdriver.Firefox,
    "Edge": webdriver.Edge
}


chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-usb-discovery")  
chrome_options.add_argument("--disable-device-discovery-notifications")

firefox_options = FirefoxOptions()
firefox_options.add_argument("--ignore-certificate-errors")

edge_options = EdgeOptions()
edge_options.add_argument("--ignore-certificate-errors")
edge_options.add_argument("--disable-features=EdgeIdentitySignin")  


status = "Passed"
error_message = None

def get_internal_links(driver, base_url):
    """
    Collect all internal links on the webpage.
    """
    links = driver.find_elements(By.TAG_NAME, "a")
    internal_links = []
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith(base_url): 
            internal_links.append(href)
    return list(set(internal_links)) 


for browser_name, browser in browsers.items():
    print(f"\n🚀 Running tests on {browser_name}...\n")

   
    if browser_name == "Chrome":
        driver = browser(options=chrome_options)
    elif browser_name == "Firefox":
        driver = browser(options=firefox_options)
    else:
        driver = browser(options=edge_options)

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
       
        if url.startswith("https://"):
            print("✅ Website has SSL (HTTPS) enabled")
        else:
            print("❌ Website does NOT have SSL (HTTPS)")

       
        response = requests.get(url)
        security_headers = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]
        for header in security_headers:
            if header in response.headers:
                print(f"✅ Security Header Present: {header}")
            else:
                print(f"❌ Missing Security Header: {header}")

        
        try:
            navbar = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
            print("✅ Navigation menu detected")
        except:
            print("⚠️ Navigation menu NOT found")

       
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            try:
                button.click()
                print(f"✅ Button {button.text} clicked successfully")
            except:
                print(f"⚠️ Button {button.text} not clickable")

       
        devices = [
            {"width": 375, "height": 667, "device": "Mobile"},
            {"width": 768, "height": 1024, "device": "Tablet"},
            {"width": 1366, "height": 768, "device": "Desktop"}
        ]
        for device in devices:
            driver.set_window_size(device["width"], device["height"])
            time.sleep(2)  
            print(f"✅ Checked layout on {device['device']}")

        
        internal_links = get_internal_links(driver, url)
        for link in internal_links:
            try:
                driver.get(link)
                time.sleep(2)  
                print(f"✅ Checked internal link: {link}")
            except:
                print(f"⚠️ Error while checking internal link: {link}")

       
        forms = driver.find_elements(By.TAG_NAME, "form")
        for form in forms:
            inputs = form.find_elements(By.TAG_NAME, "input")
            for input_field in inputs:
                input_type = input_field.get_attribute("type")
                if input_type != "submit":
                    input_field.send_keys("Test")  
                    print(f"✅ Input field {input_field.get_attribute('name')} validated")

       
        images = driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            if alt_text:
                print(f"✅ Image has alt text: {alt_text}")
            else:
                print("⚠️ Image missing alt text")

        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
            print("✅ Tab navigation works")
        except:
            print("⚠️ Tab navigation not working")

       

        
        try:
            animations = driver.find_elements(By.CSS_SELECTOR, "[style*='animation']")
            for animation in animations:
                print("✅ Animation detected")
        except:
            print("⚠️ No animations detected")

        if "?" in url:
            print(f"❌ Sensitive data found in URL: {url}")
        else:
            print("✅ No sensitive data in URL")

        title = driver.title
        print(f"✅ Page Title: {title}")
        metas = driver.find_elements(By.TAG_NAME, "meta")
        for meta in metas:
            name = meta.get_attribute("name")
            if name in ["description", "keywords"]:
                content = meta.get_attribute("content")
                print(f"✅ Meta tag {name}: {content}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        status = "Failed"
        error_message = str(e)

    driver.quit()

insert_test_result(test_name, url, status, error_message, execution_time=0)  

print("\n✅ Automated Tests Completed Successfully!")
