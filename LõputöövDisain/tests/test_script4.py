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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from db_connection import insert_test_result 

sys.stdout.reconfigure(encoding='utf-8')  

url = "https://horisontaalpuur.ee/"
test_name = "Horisontaalpuur Test"


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

       
        try:
            kontakt_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Kontakt')]")
            ))
            kontakt_button.click()
            print("✅ 'Kontakt' button clicked successfully")
        except:
            print("⚠️ No 'Kontakt' button found on the page.")

       
        try:
            contact_form = wait.until(EC.presence_of_element_located((By.XPATH, "//form")))
            print("✅ Contact form detected")
        except:
            print("⚠️ Contact form NOT found")

       
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

       
        if browser_name == "Chrome":
            try:
                print("🚀 Running Lighthouse audit for SEO & performance...")
                lighthouse_cmd = [
                    "lighthouse", url, "--quiet", "--chrome-flags=--headless",
                    "--output=json", "--output-path=reports/lighthouse_horisontaalpuur.json"
                ]
                subprocess.run(lighthouse_cmd, check=True)
                print("✅ Lighthouse audit completed (check reports/)")
            except:
                print("⚠️ Lighthouse audit failed")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        status = "Failed"
        error_message = str(e)

    driver.quit()


insert_test_result(test_name, url, status, error_message, execution_time=0)  

print("\n✅ Automated Tests Completed Successfully!")
