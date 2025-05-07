import subprocess
import sys
import os
import re
from datetime import datetime
from db.db_connection import insert_test_result  


sys.stdout.reconfigure(encoding='utf-8')


today_date = datetime.today().strftime('%Y-%m-%d')


tests_folder = "tests"


test_scripts = [f for f in os.listdir(tests_folder) if f.endswith(".py")]


def clean_execution_time(time_str):
    try:
       
        time_str = time_str.strip().lower()
        
        time_str = re.sub(r'[^\d\.]', '', time_str)
        return float(time_str) if time_str else 0.0  
    except ValueError:
        return 0.0  


for test_script in test_scripts:
    script_path = os.path.join(tests_folder, test_script)

    if not os.path.exists(script_path):
        print(f"❌ Error: Test script '{script_path}' not found!")
        continue

    
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

   
    match = re.search(r'url\s*=\s*"(https?://[^\s]+)"', script_content)

    if match:
        url = match.group(1)  
    else:
        print(f"❌ Error: No URL found in {test_script}")
        continue

    try:

        result = subprocess.run(
            ["python", script_path],
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'  
        )

        
        execution_time = clean_execution_time(result.stdout)

       
        insert_test_result(test_name=test_script, url=url, status="Passed", error_message=None, execution_time=execution_time)

        print(f"✅ {url}: Test Passed\n{result.stdout}")

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else "Unknown Error"

       
        execution_time = clean_execution_time(e.stderr)

   
        insert_test_result(test_name=test_script, url=url, status="Failed", error_message=error_message, execution_time=execution_time)

        print(f"❌ {url}: Test Failed\nError: {error_message}")

print("✅ Test results stored in MySQL.")
