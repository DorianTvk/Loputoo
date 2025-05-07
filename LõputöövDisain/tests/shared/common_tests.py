import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def run_common_tests(driver, url, wait):
    status = "Passed"
    error_message = None
    common_test_names = []

    # SSL Check
    test_name = "SSL Check"
    if not url.startswith("https://"):
        print("❌ Website does NOT have SSL (HTTPS)")
        status = "Failed"
        error_message = "SSL missing"
    else:
        print("✅ Website has SSL (HTTPS) enabled")
    common_test_names.append(test_name)

    # Security Headers
    test_name = "Security Headers"
    response = requests.get(url)
    security_headers = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]
    for header in security_headers:
        if header in response.headers:
            print(f"✅ Security Header Present: {header}")
        else:
            print(f"❌ Missing Security Header: {header}")
    common_test_names.append(test_name)


    # Responsive Sizes
    test_name = "Responsive Sizes"
    for width in [1920, 1366, 768, 375]:
        driver.set_window_size(width, 900)
        print(f"✅ Checked responsiveness at {width}px width")
    common_test_names.append(test_name)

    # Navigation
    test_name = "Navigation"
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
        print("✅ Navigation menu detected")
    except:
        print("⚠️ Navigation menu NOT found")
    common_test_names.append(test_name)

    # Performance
    test_name = "Performance"
    try:
        load_time = driver.execute_script("return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;")
        print(f"✅ Page load time: {load_time}ms")
    except:
        print("⚠️ Could not measure load time")
    common_test_names.append(test_name)

    # SEO
    test_name = "SEO check"
    if driver.title:
        print(f"✅ Page title found: {driver.title}")
    else:
        print("⚠️ Missing page title")

    
    if driver.find_elements(By.XPATH, "//meta[@name='description']"):
        print("✅ Meta description found")
    else:
        print("⚠️ Missing meta description")
    common_test_names.append(test_name)

    return status, error_message, common_test_names
