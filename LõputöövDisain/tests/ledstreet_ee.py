import sys
import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
from db_connection import connect_to_db, insert_test_result

from shared.browser_setup import get_browsers
from shared.common_tests import run_common_tests
from shared.screenshot import take_screenshot
from visual_regression.screenshot_util import save_screenshot
from visual_regression.image_compare import compare_images

url = "https://ledstreet.ee/"
test_name = "LED Street Contact Form Test"
browsers = get_browsers()

test_results = []

db = connect_to_db()
if db is None:
    print("❌ Could not connect to database. Exiting.")
    sys.exit(1)
else:
    print("✅ Database connection established.")

for browser_name, browser_data in browsers.items():
    print(f"\n🟡 Running test on {browser_name}...")

    start_time = time.time()
    status = "Passed"
    error_message = None
    screenshot_path = None

    try:
        driver = browser_data["driver"](options=browser_data["options"])
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        common_status, common_error, common_test_names = run_common_tests(driver, url, wait)
        if common_status == "Failed":
            status = "Failed"
            error_message = common_error

        for common_test_name in common_test_names:
            test_results.append((
                f"{common_test_name} ({browser_name})",
                url,
                status,
                error_message,
                round(time.time() - start_time, 2),
                screenshot_path,
                None, None, None,
                "regular"
            ))
        test_name = "Contact Form"
        custom_status = "Passed"
        custom_error = None
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//form")))
            print("✅ Contact form detected")
        except:
            print("⚠️ Contact form NOT found")
            custom_status = "Failed"
            custom_error = "Contact form missing"

        test_results.append((
            f"{test_name} ({browser_name})",
            url,
            custom_status,
            custom_error,
            round(time.time() - start_time, 2),
            screenshot_path,
            None, None, None,
            "regular"
        ))

        
        test_name = "Kontakt Button"
        custom_status = "Passed"
        custom_error = None
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Kontakt')]")))
            button.click()
            print("✅ 'Kontakt' button clicked")
        except:
            print("⚠️ 'Kontakt' button not found")
            custom_status = "Failed"
            custom_error = "Kontakt button missing"

        test_results.append((
            f"{test_name} ({browser_name})",
            url,
            custom_status,
            custom_error,
            round(time.time() - start_time, 2),
            screenshot_path,
            None, None, None,
            "regular"
        ))

        
        test_name = "Homepage Visual Check"
        baseline_path = save_screenshot(driver, url, test_name, is_baseline=True)
        new_path = save_screenshot(driver, url, test_name, is_baseline=False)
        diff_path = new_path.replace(".png", "_diff.png")

        visual_status = "Passed"
        visual_error = None

        if not compare_images(baseline_path, new_path, diff_path):
            visual_status = "Failed"
            visual_error = "Visual regression detected"

        test_results.append((
            f"{test_name} ({browser_name})",
            url,
            visual_status,
            visual_error,
            round(time.time() - start_time, 2),
            screenshot_path,
            baseline_path,
            new_path,
            diff_path,
            "visual"
        ))

    except Exception as e:
        print(f"❌ Test failed: {e}")
        screenshot_path = take_screenshot(driver, f"{test_name}_{browser_name}")
        status = "Failed"
        error_message = str(e)

        test_results.append((
            f"Unexpected Error ({browser_name})",
            url,
            status,
            error_message,
            round(time.time() - start_time, 2),
            screenshot_path,
            None, None, None,
            "regular"
        ))

    finally:
        driver.quit()


for result in test_results:
    insert_test_result(db, *result)


db.commit()
db.close()

print("\n✅ All browser tests completed.")